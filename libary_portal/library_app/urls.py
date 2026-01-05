from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("home/", home, name="home"),
    path("save", save_student, name="save"),
    path("shop", shopping, name="shop"),

]
