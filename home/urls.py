from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home_screen, name="home"),
    path('profile/<user_id>/', views.profile_view, name="profile"),
    
]