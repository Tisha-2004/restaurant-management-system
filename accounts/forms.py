from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from customers.models import Customer

from .models import Profile

BASE = {"class": "form-control"}


class RegisterForm(UserCreationForm):
    """Creates a User, its Profile and the matching Customer record."""

    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs=BASE))
    email = forms.EmailField(widget=forms.EmailInput(attrs=BASE))
    mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs=BASE))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={**BASE, "rows": 2}))

    class Meta:
        model = User
        fields = ["username", "full_name", "email", "mobile", "address", "password1", "password2"]
        widgets = {"username": forms.TextInput(attrs=BASE)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("password1", "password2"):
            self.fields[name].widget.attrs.update(BASE)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["full_name"]
        user.save()
        Profile.objects.create(user=user, role=Profile.CUSTOMER, mobile=self.cleaned_data["mobile"])
        Customer.objects.create(
            user=user,
            name=self.cleaned_data["full_name"],
            mobile=self.cleaned_data["mobile"],
            email=user.email,
            address=self.cleaned_data.get("address", ""),
        )
        return user


class StyledLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(BASE)


class UserForm(forms.ModelForm):
    """Used by the admin Users module."""

    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs=BASE),
            "first_name": forms.TextInput(attrs=BASE),
            "email": forms.EmailInput(attrs=BASE),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
