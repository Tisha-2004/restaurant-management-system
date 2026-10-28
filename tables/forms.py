from django import forms

from .models import RestaurantTable

BASE = {"class": "form-control"}


class TableForm(forms.ModelForm):
    class Meta:
        model = RestaurantTable
        fields = ["number", "capacity", "status"]
        widgets = {
            "number": forms.NumberInput(attrs={**BASE, "min": "1"}),
            "capacity": forms.NumberInput(attrs={**BASE, "min": "1"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
