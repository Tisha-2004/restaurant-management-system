from django import forms
from django.utils import timezone

from .models import Reservation

BASE = {"class": "form-control"}

WIDGETS = {
    "customer": forms.Select(attrs={"class": "form-select"}),
    "table": forms.Select(attrs={"class": "form-select"}),
    "date": forms.DateInput(attrs={**BASE, "type": "date"}),
    "time": forms.TimeInput(attrs={**BASE, "type": "time"}),
    "guests": forms.NumberInput(attrs={**BASE, "min": "1"}),
    "status": forms.Select(attrs={"class": "form-select"}),
    "note": forms.TextInput(attrs=BASE),
}


class ReservationValidationMixin:
    """Shared rules: no past dates and never overbook a table's capacity."""

    def clean(self):
        cleaned = super().clean()
        date, table, guests = cleaned.get("date"), cleaned.get("table"), cleaned.get("guests")
        if date and date < timezone.localdate():
            self.add_error("date", "Reservation date cannot be in the past.")
        if table and guests and guests > table.capacity:
            self.add_error("guests", f"Table {table.number} seats only {table.capacity} guests.")
        return cleaned


class ReservationForm(ReservationValidationMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["customer", "table", "date", "time", "guests", "status", "note"]
        widgets = WIDGETS


class PublicReservationForm(ReservationValidationMixin, forms.ModelForm):
    """Reservation form for logged-in customers (customer comes from the session)."""

    class Meta:
        model = Reservation
        fields = ["table", "date", "time", "guests", "note"]
        widgets = WIDGETS
