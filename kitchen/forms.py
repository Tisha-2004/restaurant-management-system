from django import forms
from django.forms import inlineformset_factory

from .models import Order, OrderItem

BASE = {"class": "form-control"}


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "table", "status"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "table": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={**BASE, "min": "1"}),
        }

    def has_changed(self):
        """Treat rows without a dish selected as untouched extra rows."""
        if not self.instance.pk and not self.data.get(self.add_prefix("item")):
            return False
        return super().has_changed()


# Order + its lines are edited on a single screen
OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3, can_delete=True)
