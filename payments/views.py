import stripe

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from decimal import Decimal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from shop.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid
            order.paid = True
            order.save()
    return HttpResponse(status=200)


@login_required
def payment_process(request):
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("payments:completed"))
        cancel_url = request.build_absolute_uri(reverse("payments:canceled"))
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        for item in order.items.all():
            if int(item.product.quantity) < int(item.quantity):
                return redirect(reverse("payments:canceled"))
            item.product.quantity = int(item.product.quantity) - int(item.quantity)
            item.product.save()
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "usd",
                        "product_data": {
                            "name": item.product.title,
                        },
                    },
                    "quantity": item.quantity,
                }
            )
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    return render(request, "payments/process.html", locals())


@login_required
def payment_completed(request):
    return render(request, "payments/completed.html")


@login_required
def payment_canceled(request):
    return render(request, "payments/canceled.html")


@login_required
def payment_orders_clear(request):
    if request.method == "POST":
        orders = request.user.user_orders.all()
        orders.delete()
    return redirect(reverse("auth:order_list"))
