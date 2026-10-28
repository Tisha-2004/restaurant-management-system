from django.db import models
from django.utils import timezone

from customers.models import Customer
from menu.models import MenuItem
from tables.models import RestaurantTable


class Order(models.Model):
    PENDING, PREPARING, READY, SERVED = "pending", "preparing", "ready", "served"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PREPARING, "Preparing"),
        (READY, "Ready"),
        (SERVED, "Served"),
    ]

    number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    table = models.ForeignKey(
        RestaurantTable, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.number:
            # Human friendly sequential order number, e.g. ORD-000042
            last_id = Order.objects.order_by("-id").values_list("id", flat=True).first() or 0
            self.number = f"ORD-{last_id + 1:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number

    @property
    def total(self):
        return sum((line.subtotal for line in self.items.all()), 0)

    @property
    def badge(self):
        return {self.PENDING: "secondary", self.PREPARING: "warning", self.READY: "info", self.SERVED: "success"}[
            self.status
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.item.price * self.quantity
