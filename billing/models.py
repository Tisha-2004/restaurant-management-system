from decimal import Decimal

from django.db import models
from django.utils import timezone

from customers.models import Customer
from kitchen.models import Order
from menu.models import MenuItem


class Bill(models.Model):
    CASH, CARD, UPI = "cash", "card", "upi"
    METHOD_CHOICES = [(CASH, "Cash"), (CARD, "Card"), (UPI, "UPI")]
    PAID, UNPAID = "paid", "unpaid"
    PAYMENT_STATUS = [(PAID, "Paid"), (UNPAID, "Unpaid")]

    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bills")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="bills")
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("5"))
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=CASH)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default=UNPAID)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_id = Bill.objects.order_by("-id").values_list("id", flat=True).first() or 0
            self.invoice_number = f"INV-{last_id + 1:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

    @property
    def subtotal(self):
        return sum((line.subtotal for line in self.items.all()), Decimal("0"))

    @property
    def gst_amount(self):
        return (self.subtotal * self.gst_percent / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def grand_total(self):
        return (self.subtotal + self.gst_amount).quantize(Decimal("0.01"))


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
