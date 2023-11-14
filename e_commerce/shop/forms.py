from django import forms
from django.core import validators
from django.db.models import Max

from shop.models import Product, Review, ProductType, ProductBrand, ProductStyle, Order


class NewsletterForm(forms.Form):
    email = forms.CharField(
        max_length=300,
        widget=forms.TextInput({"placeholder": "Enter your email address"}),
        validators=[validators.EmailValidator()],
    )


class ProductFilterForm(forms.Form):
    FILTER_BY = [
        ("NA", "New Arrivals"),
        ("MP", "Most Popular"),
        ("MO", "Most Ordered"),
    ]
    BRANDS = [(query.name, query.name) for query in ProductBrand.objects.all()]
    STYLES = [(query.name, query.name) for query in ProductStyle.objects.all()]
    TYPES = [(query.name, query.name) for query in ProductType.objects.all()]
    max_price = Product.objects.aggregate(price=Max("price"))["price"]

    min_price = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "value": "0",
                "max": str(max_price),
                "oninput": "slideOne()",
                "id": "slider-1",
                "min": "0",
            }
        ),
        required=False,
        label="",
    )
    max_price = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "value": "100",
                "min": "0",
                "max": str(max_price),
                "oninput": "slideTwo()",
                "id": "slider-2",
            }
        ),
        required=False,
        label="",
    )

    filter_by = forms.ChoiceField(
        choices=FILTER_BY, widget=forms.Select, label="Filter By", required=False
    )
    gender = forms.ChoiceField(
        choices=Product.ProductGender.choices,
        widget=forms.Select,
        label="Choose gender",
        required=False,
    )
    type = forms.ChoiceField(
        choices=TYPES, widget=forms.Select, label="Choose type", required=False
    )
    brand = forms.ChoiceField(
        choices=BRANDS, widget=forms.Select, label="Choose brand", required=False
    )
    style = forms.ChoiceField(
        choices=STYLES, widget=forms.Select, label="Choose style", required=False
    )


class ProductCartForm(forms.Form):
    quantity = forms.IntegerField(
        max_value=100,
        min_value=1,
        validators=[validators.MaxValueValidator(100), validators.MinValueValidator(1)],
    )

    def __init__(self, product: Product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sizes = product.sizes.all()
        size_choices = [(size, size) for size in sizes]
        self.fields["sizes"] = forms.ChoiceField(
            choices=size_choices, widget=forms.RadioSelect
        )
        self.fields["quantity"] = forms.IntegerField(
            max_value=product.quantity,
            min_value=1,
            validators=[
                validators.MaxValueValidator(product.quantity),
                validators.MinValueValidator(1),
            ],
        )


class ProductReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        ("5", "Awesome - 5 stars"),
        ("4.5", "Pretty good - 4.5 stars"),
        ("4", "Pretty good - 4 stars"),
        ("3.5", "Meh - 3.5 stars"),
        ("3", "Meh - 3 stars"),
        ("2.5", "Kinda bad - 2.5 stars"),
        ("2", "Kinda bad - 2 stars"),
        ("1.5", "Meh - 1.5 stars"),
        ("1", "Sucks big time - 1 star"),
        ("0.5", "Sucks big time - 0.5 stars"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Review
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"cols": 79, "rows": 20})}
        labels = {"body": "Write your review"}


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "postal_code",
            "city",
        ]
