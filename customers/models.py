from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    """A restaurant guest. Optionally linked to a login account."""

    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer"
    )
    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to="customers/", blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.name} ({self.mobile})"
