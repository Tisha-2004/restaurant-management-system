from django import forms
from django.forms import inlineformset_factory

from .models import Bill, BillItem

BASE = {"class": "form-control"}


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ["customer", "order", "gst_percent", "payment_method", "payment_status"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "order": forms.Select(attrs={"class": "form-select"}),
            "gst_percent": forms.NumberInput(attrs={**BASE, "step": "0.01", "min": "0"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "payment_status": forms.Select(attrs={"class": "form-select"}),
        }


class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ["item", "quantity", "price"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-select item-select"}),
            "quantity": forms.NumberInput(attrs={**BASE, "min": "1"}),
            "price": forms.NumberInput(attrs={**BASE, "step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["price"].required = False

    def has_changed(self):
        """Treat rows without a dish selected as untouched extra rows."""
        if not self.instance.pk and not self.data.get(self.add_prefix("item")):
            return False
        return super().has_changed()

    def clean(self):
        cleaned = super().clean()
        # Fall back to the current menu price when the cashier leaves price blank
        if not cleaned.get("price") and cleaned.get("item"):
            cleaned["price"] = cleaned["item"].price
        return cleaned


BillItemFormSet = inlineformset_factory(Bill, BillItem, form=BillItemForm, extra=3, can_delete=True)
