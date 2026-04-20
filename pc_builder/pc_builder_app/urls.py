from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path('builder/', views.builder, name='builder'),
    path('builder/<int:list_number>/', views.builder_edit, name='builder_edit'),
    path('builder/<int:list_number>/select/<str:part_type>/', views.builder_select_part, name='builder_select_part'),
    path('builder/<int:list_number>/remove/<int:list_part_id>/', views.builder_remove, name='builder_remove'),
    path('builder/delete/<int:list_number>/', views.builder_delete, name='builder_delete'),

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


    path('browse/', views.customer_browse, name='customer_browse'),
    path('component/<int:list_part_id>/', views.component_detail, name='component_detail'), 

]