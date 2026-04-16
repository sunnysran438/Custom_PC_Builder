from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("builder/", views.builder, name="builder"),
    path("search/", views.search, name="search"),

    path("add/<int:component_id>/", views.add_component, name="add_component"),
    path("remove/<int:item_id>/", views.remove_component, name="remove_component"),

    path("supplier_inventory/", views.supplier_inventory, name="supplier_inventory"),
    path("manufacturer/", views.manufacturer, name="manufacturer"),
]