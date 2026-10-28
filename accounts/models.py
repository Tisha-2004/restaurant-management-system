from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Extra data on top of the built-in User, mainly the staff role."""

    CUSTOMER, STAFF, CHEF, ADMIN = "customer", "staff", "chef", "admin"
    ROLE_CHOICES = [(CUSTOMER, "Customer"), (STAFF, "Staff"), (CHEF, "Chef"), (ADMIN, "Admin")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    mobile = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_staff_member(self):
        return self.role in {self.STAFF, self.CHEF, self.ADMIN}
