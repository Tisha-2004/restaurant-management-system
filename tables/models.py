from django.db import models


class RestaurantTable(models.Model):
    AVAILABLE, RESERVED, OCCUPIED = "available", "reserved", "occupied"
    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (RESERVED, "Reserved"),
        (OCCUPIED, "Occupied"),
    ]

    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number}"

    @property
    def color(self):
        """Bootstrap colour used for the colour-coded table cards."""
        return {self.AVAILABLE: "success", self.RESERVED: "warning", self.OCCUPIED: "danger"}[self.status]
