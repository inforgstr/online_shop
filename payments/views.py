from django.shortcuts import render


def product_page(request):
    return render(request, "payments/")

def payment_successfull(request):
    return render(request, "payments/")

def payment_cancelled(request):
    return render(request, "payments/")

def stripe_webhook(request):
    return render(request, "payments/")
