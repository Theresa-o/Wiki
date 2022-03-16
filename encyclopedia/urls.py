from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entrypage"),
    path("search", views.search, name="search"),
    path("add_page", views.add_page, name="addpage"),
    path("edit_page/<str:title>", views.edit_page, name="editpage"),
    path("random_page", views.random_page, name="randompage")


]
