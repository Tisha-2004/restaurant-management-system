from django.db import models

from customers.models import Customer
from tables.models import RestaurantTable


class Reservation(models.Model):
    AVAILABLE, RESERVED, COMPLETED, CANCELLED = "available", "reserved", "completed", "cancelled"
    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (RESERVED, "Reserved"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reservations")
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE, related_name="reservations")
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=RESERVED)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.customer.name} - Table {self.table.number} on {self.date}"

    @property
    def badge(self):
        return {
            self.AVAILABLE: "secondary",
            self.RESERVED: "warning",
            self.COMPLETED: "success",
            self.CANCELLED: "danger",
        }[self.status]
