from django.contrib import admin

from django.urls import path
from home import views

urlpatterns = [
    path('', views.login_view,name='login'),
    path('signin/',views.register,name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('home/',views.home_view, name = 'home'),
] 
