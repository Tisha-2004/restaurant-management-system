from django.contrib import admin

from .models import ContactMessage, GalleryImage, RestaurantSetting, Testimonial

admin.site.register([RestaurantSetting, GalleryImage, Testimonial, ContactMessage])
