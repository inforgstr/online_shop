from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
)

from auth.forms import (
    UserLoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
    ProfileRegistrationForm,
    UserChangePasswordForm,
    CustomPasswordResetForm,
)
from cart.cart import Cart


def user_login(request):
    if request.user.is_authenticated:
        return redirect("shop:home")

    if request.method == "POST":
        prev_cart = Cart(request).cart
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if prev_cart:
                        cart = Cart(request)
                        cart.refresh(prev_cart)
                    next_url = request.GET.get("next")
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect(reverse("shop:home"))
        messages.error(request, "Username or email does not match.")
        return redirect(reverse("auth:login"))
    else:
        form = UserLoginForm()

    return render(request, "auth/login.html", {"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse("shop:home"))

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.first_name = form.cleaned_data["first_name"]
            new_user.save()
            new_user.profile.phone_number = profile_form.cleaned_data["phone_number"]
            new_user.profile.save()
            messages.success(
                request, "Account has successfully authorized! Login to access"
            )
            return redirect(reverse("auth:login"))
        return render(
            request, "auth/signup.html", {"form": form, "profile_form": profile_form}
        )
    else:
        form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(
        request, "auth/signup.html", {"form": form, "profile_form": profile_form}
    )


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("auth:login"))


@login_required
def user_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has successfully updated")
        else:
            messages.error(request, f"{user_form.errors or profile_form.errors}")
        return redirect(reverse("auth:user_profile"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "profile/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_change_password(request):
    if request.method == "POST":
        user = request.user
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            is_user = user.check_password(form.cleaned_data["old_password"])
            if is_user:
                psw = form.cleaned_data["password2"]
                user.set_password(psw)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has successfully changed")
                return redirect(reverse("auth:user_profile"))
            messages.error(request, "Incorrect Old Password was given.")
        return render(request, "auth/change_password.html", {"form": form})
    else:
        form = UserChangePasswordForm()
    return render(request, "auth/change_password.html", {"form": form})


@login_required
def order_list(request):
    user_orders = request.user.user_orders.all().order_by("-created")
    return render(request, "order/order_list.html", {"orders": user_orders})


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("auth:password_reset_done")
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("auth:password_reset_complete")
