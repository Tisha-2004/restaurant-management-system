from django import forms

from .models import Customer

BASE = {"class": "form-control"}


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "mobile", "email", "address", "photo"]
        widgets = {
            "name": forms.TextInput(attrs=BASE),
            "mobile": forms.TextInput(attrs=BASE),
            "email": forms.EmailInput(attrs=BASE),
            "address": forms.Textarea(attrs={**BASE, "rows": 3}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"].strip()
        digits = mobile.replace("+", "").replace(" ", "")
        if not digits.isdigit() or not 10 <= len(digits) <= 13:
            raise forms.ValidationError("Enter a valid mobile number (10-13 digits).")
        return mobile
