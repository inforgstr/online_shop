from django.conf import settings

from shop.models import Product, CartItem, Size


class Cart:
    def __init__(self, request) -> None:
        """
        Initialize the cart.
        """
        self.request = request
        self.session = request.session
        self.is_auth = request.user.is_authenticated
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        if "is_subs" not in self.session:
            self.session["is_subs"] = False
        if self.is_auth:
            self.user_carts = self.user.user_carts.all()
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            if self.is_auth and self.user_carts.exists():
                for query in self.user_carts:
                    product_id = f"{query.product.pk},{query.size.name}"
                    cart[product_id] = {
                        "quantity": int(query.quantity),
                        "price": float(query.get_price()),
                    }

        self.cart = cart

    def _refresh_session(self):
        """
        Refresh user session from user db cart.
        """
        self.cart = self.session[settings.CART_SESSION_ID] = {}
        if self.is_auth and self.user_carts.exists():
            for query in self.user_carts:
                product_id = f"{query.product.pk},{query.size.name}"
                self.cart[product_id] = {
                    "quantity": int(query.quantity),
                    "price": float(query.get_price()),
                }

    def _refresh_db(self):
        """
        Refresh user cart db from user session.
        """
        if not self.cart or not self.is_auth:
            return False
        for product_id in self.cart:
            id, size = product_id.split(",")
            q = self.cart[product_id]["quantity"]
            try:
                size_obj = Size.objects.get(name=size)
                product = Product.objects.get(id=id)
            except Size.DoesNotExist:
                continue
            user_cart = CartItem.objects.filter(
                user=self.user, product=product, size=size_obj
            )
            if not user_cart.exists():
                CartItem.objects.create(
                    user=self.user, product=product, size=size_obj, quantity=int(q)
                )

    def refresh(self, cart_values):
        """
        Refresh user session cart from previous data.
        """
        if self.is_auth:
            self._refresh_db()
            self._refresh_session()
            self.cart.update(cart_values)
            self.save()

    def add(self, product: Product, quantity: str | int, size_name: str) -> bool:
        product_id = f"{product.pk},{size_name}"
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.get_discounted_price()),
            }
        self.save()

        added = True
        if self.is_auth:
            added = product.add_cart(self.user, size_name, int(quantity))
        cart_qty = self.cart[product_id]["quantity"]

        if (
            (int(quantity) < 0 and int(cart_qty) > 1)
            or (int(quantity) > 0 and int(product.quantity) > int(quantity))
        ) and added:
            self.cart[product_id]["quantity"] += int(quantity)
            self.save()
            return True
        return False

    def remove(self, product: Product, size_name: str) -> bool:
        """
        Remove a product from the cart.
        """
        product_id = f"{product.pk},{size_name}"
        removed = True
        if self.is_auth:
            removed = product.remove_cart(self.user, size_name)
        if product_id in self.cart and removed:
            del self.cart[product_id]
            self.save()
            return True
        return False

    def clear(self):
        """
        Remove all product exists in the cart.
        """
        if self.is_auth:
            CartItem.objects.filter(user=self.user).delete()
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def __iter__(self):
        product_ids = [int(data.split(",")[0]) for data in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        product_dict = {product.pk: product for product in products}

        for key, item in cart.items():
            item_id, size_name = key.split(",")
            product = product_dict.get(int(item_id))
            data = {
                "pk": product.pk,
                "title": product.title,
                "slug": product.slug,
                "img1": product.image1_url,
                "img2": product.image2_url,
                "img3": product.image3_url,
                "title": product.title,
                "url": product.get_absolute_url(),
            }
            item["product"] = data
            item["discount"] = product.discount
            item["size"] = size_name
            item["price"] = float(item["price"])
            yield item

    def get_total_price(self):
        return sum(
            int(value["quantity"]) * value["price"] for key, value in self.cart.items()
        )
