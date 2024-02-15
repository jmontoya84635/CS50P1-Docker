from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.searchResult, name="searchResult"),
    path("search", views.searchBar, name="searchBar"),
    path("addPage/", views.addPage, name="addPage"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random/", views.randomEntry, name="randomPage"),
]
