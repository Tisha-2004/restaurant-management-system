from django.urls import path

from . import views

app_name = "kitchen"

urlpatterns = [
    path("", views.kitchen_dashboard, name="dashboard"),
    path("orders/", views.order_list, name="list"),
    path("orders/add/", views.order_add, name="add"),
    path("orders/<int:pk>/", views.order_detail, name="detail"),
    path("orders/<int:pk>/edit/", views.order_edit, name="edit"),
    path("orders/<int:pk>/delete/", views.order_delete, name="delete"),
    path("orders/<int:pk>/status/<str:status>/", views.order_status, name="status"),
]
