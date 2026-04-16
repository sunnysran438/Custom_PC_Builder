from django.shortcuts import render, redirect
from .models import Build, BuildItem, Component


def home(request):
    return render(request, "index.html")


def login(request):
    return render(request, "customer_login.html")


def register(request):
    return render(request, "customer_registeration.html")


def builder(request):
    build, created = Build.objects.get_or_create(id=1, defaults={"name": "My Build"})
    items = BuildItem.objects.filter(build=build)

    return render(request, "builder.html", {"items": items})


def search(request):
    components = Component.objects.all()
    return render(request, "search_page.html", {"components": components})


def add_component(request, component_id):
    build = Build.objects.get(id=1)
    component = Component.objects.get(id=component_id)

    BuildItem.objects.create(build=build, component=component)
    return redirect("builder")


def remove_component(request, item_id):
    BuildItem.objects.filter(id=item_id).delete()
    return redirect("builder")


def supplier_inventory(request):
    return render(request, "supplier_inventory_page.html")


def manufacturer(request):
    return render(request, "manufacturer_selection_page.html")