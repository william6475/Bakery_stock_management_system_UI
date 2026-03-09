"""
URL configuration for Bakery_stock_management_UI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from stock_management_ui import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('manage_branches/', views.manage_branches, name='manage_branches'),
    path('manage_item_types/', views.manage_item_types, name='manage_item_types'),
    path('manage_stock/', views.manage_stock, name='manage_stock'),
    path('manage_sales/', views.manage_sales, name='manage_sales'),
]
