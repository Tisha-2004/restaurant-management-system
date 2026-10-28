from django import forms

from .models import Category, MenuItem

BASE = {"class": "form-control"}


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "category", "price", "description", "image", "image_url", "is_available", "is_popular"]
        widgets = {
            "name": forms.TextInput(attrs=BASE),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={**BASE, "step": "0.01", "min": "0"}),
            "description": forms.Textarea(attrs={**BASE, "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*", "id": "imageInput"}),
            "image_url": forms.URLInput(attrs=BASE),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_popular": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "icon", "image_url"]
        widgets = {
            "name": forms.TextInput(attrs=BASE),
            "icon": forms.TextInput(attrs=BASE),
            "image_url": forms.URLInput(attrs=BASE),
        }
