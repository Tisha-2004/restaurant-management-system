from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("", views.reservation_list, name="list"),
    path("add/", views.reservation_add, name="add"),
    path("book/", views.book_table, name="book"),
    path("calendar/", views.reservation_calendar, name="calendar"),
    path("<int:pk>/edit/", views.reservation_edit, name="edit"),
    path("<int:pk>/delete/", views.reservation_delete, name="delete"),
    path("<int:pk>/cancel/", views.reservation_cancel, name="cancel"),
]
