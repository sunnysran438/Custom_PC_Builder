from django.urls import path
from . import views 


urlpatterns = [
    path("", views.home, name ="home"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('builder/', views.builder, name='builder'),
    path('search/', views.search, name='search'),
    path('supplier_inventory/', views.supplier_inventory, name='supplier_inventory'),
    path('manufacturer/', views.manufacturer, name='manufacturer'),
]