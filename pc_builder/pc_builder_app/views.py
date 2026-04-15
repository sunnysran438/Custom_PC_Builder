from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "index.html")


def login(request):
    return render(request, 'customer_login.html')

def register(request):
    return render(request, 'customer_registeration.html')

def builder(request):
    return render(request, 'builder.html')

def search(request):
    return render(request, 'search_page.html')

def supplier_inventory(request):
    return render(request, 'supplier_inventory_page.html')

def manufacturer(request):
    return render(request, 'manufacturer_selection_page.html')

