from django import forms

from .models import ContactMessage, RestaurantSetting

BASE = {"class": "form-control"}


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs=BASE),
            "email": forms.EmailInput(attrs=BASE),
            "subject": forms.TextInput(attrs=BASE),
            "message": forms.Textarea(attrs={**BASE, "rows": 4}),
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = RestaurantSetting
        fields = [
            "name", "tagline", "logo", "phone", "email", "address",
            "opening_hours", "gst_percent", "facebook", "instagram", "twitter",
        ]
        widgets = {
            "name": forms.TextInput(attrs=BASE),
            "tagline": forms.TextInput(attrs=BASE),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "phone": forms.TextInput(attrs=BASE),
            "email": forms.EmailInput(attrs=BASE),
            "address": forms.TextInput(attrs=BASE),
            "opening_hours": forms.TextInput(attrs=BASE),
            "gst_percent": forms.NumberInput(attrs=BASE),
            "facebook": forms.URLInput(attrs=BASE),
            "instagram": forms.URLInput(attrs=BASE),
            "twitter": forms.URLInput(attrs=BASE),
        }
