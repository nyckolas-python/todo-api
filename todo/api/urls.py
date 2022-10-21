from django.urls import include, path
from rest_framework import routers
from api import views

from django.contrib import admin

urlpatterns = [
    path('login/', views.user_login),
    path('create-user/', views.CreateUser.as_view())
]