from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView

from auth import views


app_name = "auth"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("sign-up/", views.register, name="signup"),
    path("user-profile/", views.user_profile, name="user_profile"),
    path(
        "user-change-password/", views.user_change_password, name="user_change_password"
    ),
    # Reset Password
    path(
        "user-reset-password/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "user-reset-password/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "user-reset-password/confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "user-reset-password/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "user-orders/",
        views.order_list,
        name="order_list",
    ),
]
