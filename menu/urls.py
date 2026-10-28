from django.urls import path

from . import views

app_name = "menu"

urlpatterns = [
    path("", views.menu_list, name="list"),
    path("manage/", views.menu_manage, name="manage"),
    path("add/", views.menu_add, name="add"),
    path("categories/", views.category_list, name="categories"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("<int:pk>/", views.menu_detail, name="detail"),
    path("<int:pk>/edit/", views.menu_edit, name="edit"),
    path("<int:pk>/delete/", views.menu_delete, name="delete"),
]
