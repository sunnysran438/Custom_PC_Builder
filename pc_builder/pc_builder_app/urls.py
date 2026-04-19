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
    path('supplier/', views.supplier_inventory, name='supplier'),
    path('supplier/supplier_search_page/', views.supplier_search_page, name='supplier_search_page'),
    path('supplier/add-item/', views.supplier_add_item, name='supplier_add_item'),
    path('supplier/update-item/', views.supplier_update_item, name='supplier_update_item'),


    path("manufacturer/", views.manufacturer, name="manufacturer"),
    path('logout/', views.logout, name='logout'),
    path('my-components/', views.view_my_components, name='view_my_components'),
    path('delete-component/<int:part_id>/', views.delete_component, name='delete_component'),

]