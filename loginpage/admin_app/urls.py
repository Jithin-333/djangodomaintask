from django.contrib import admin
from django.urls import path, include
from admin_app import views as admin_views



urlpatterns = [
    path('admin_home/',admin_views.admin_home, name='admin_home'),
    path('edit_user/<id>',admin_views.edit_user, name = 'edit_user'),
    path('admin_search/',admin_views.admin_search, name = 'admin_search'),
    path('delete_user/<id>',admin_views.delete_user, name = 'delete_user'),
    path('create_user/',admin_views.create_user, name = 'create_user'),
] 