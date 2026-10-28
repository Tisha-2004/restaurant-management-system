"""Site-wide models: restaurant settings, gallery, testimonials, contact messages."""
from django.db import models


class RestaurantSetting(models.Model):
    """Singleton-style model holding branding/contact info shown across the site."""

    name = models.CharField(max_length=120, default="Spice Symphony")
    tagline = models.CharField(max_length=200, default="Delicious Food, Delivered With Love")
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    phone = models.CharField(max_length=20, default="+91 98250 12345")
    email = models.EmailField(default="hello@spicesymphony.com")
    address = models.CharField(max_length=255, default="12 Marine Drive, Ahmedabad, Gujarat 380009")
    opening_hours = models.CharField(max_length=120, default="Mon - Sun : 11:00 AM - 11:30 PM")
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    facebook = models.URLField(blank=True, default="https://facebook.com")
    instagram = models.URLField(blank=True, default="https://instagram.com")
    twitter = models.URLField(blank=True, default="https://twitter.com")

    class Meta:
        verbose_name = "Restaurant Setting"

    def __str__(self):
        return self.name

    @classmethod
    def load(cls):
        """Return the single settings row, creating it on first access."""
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj


class GalleryImage(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="Used when no file is uploaded")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def src(self):
        return self.image.url if self.image else self.image_url


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True, default="Guest")
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    avatar_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"
