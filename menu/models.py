from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    icon = models.CharField(max_length=60, default="fa-solid fa-utensils")
    image_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=140)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="menu_images/", blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="Fallback image when no file is uploaded")
    is_available = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def src(self):
        return self.image.url if self.image else self.image_url
