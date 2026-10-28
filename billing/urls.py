from django.urls import path

from . import views

app_name = "billing"

urlpatterns = [
    path("", views.bill_list, name="list"),
    path("add/", views.bill_add, name="add"),
    path("<int:pk>/", views.bill_detail, name="detail"),
    path("<int:pk>/edit/", views.bill_edit, name="edit"),
    path("<int:pk>/delete/", views.bill_delete, name="delete"),
    path("<int:pk>/pdf/", views.bill_pdf, name="pdf"),
    path("<int:pk>/paid/", views.bill_mark_paid, name="mark_paid"),
]
