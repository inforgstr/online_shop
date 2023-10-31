from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

from shop.models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Username or Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "* Password"}),
        validators=[
            validators.MinLengthValidator(8),
        ],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "* Repeat Password"}),
        validators=[
            validators.MinLengthValidator(8),
        ],
    )

    class Meta:
        model = User
        fields = ["first_name", "username", "email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "* Email"}),
            "username": forms.TextInput(attrs={"placeholder": "* Username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
        }
        required = [
            "username",
            "email",
            "password",
            "password2",
        ]
        labels = {
            "first_name": "",
            "username": "",
            "email": "",
            "password": "",
            "password2": "",
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data


class ProfileRegistrationForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"maxlength": 13, "type": "tel", "placeholder": "* Phone Number"}
        ),
        required=True,
        validators=[validators.MaxLengthValidator(limit_value=13)],
    )

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"]
        qs = Profile.objects.filter(phone_number=phone)
        if qs.exists():
            raise forms.ValidationError("Phone number already in use.")
        return phone


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
        help_texts = {
            "username": "",
        }

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "phone_number"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"type": "tel"}),
            "image": forms.ClearableFileInput(),
        }
        labels = {
            "image": "",
        }

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"]
        qs = Profile.objects.exclude(id=self.instance.id).filter(phone_number=phone)
        if qs.exists() and phone:
            raise forms.ValidationError("Phone number already in use.")
        return phone


class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Old Password"}),
        required=True,
        label="",
        validators=[validators.MinLengthValidator(8)],
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"}),
        required=True,
        label="",
        validators=[validators.MinLengthValidator(8)],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat New Password"}),
        required=True,
        label="",
        validators=[validators.MinLengthValidator(8)],
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords does not match.")
        return cd["password2"]


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter Email", "autocomplete": "email"}
        ),
    )
