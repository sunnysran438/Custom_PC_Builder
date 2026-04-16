from django.contrib import admin
from .models import Manufacturer, Supplier, Component, StoreItem, Build, BuildItem


admin.site.register(Manufacturer)
admin.site.register(Supplier)
admin.site.register(Component)
admin.site.register(StoreItem)
admin.site.register(Build)
admin.site.register(BuildItem)