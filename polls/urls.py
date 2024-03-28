from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("main", views.main, name="main"),
    path("menu", views.menu, name="menu"),
    path("order", views.order, name="order"),
]