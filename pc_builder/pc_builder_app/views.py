from django.shortcuts import render, redirect
from .models import Build, BuildItem, Component
from .models import Customer
from pc_builder_app import database_api

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def supplier_inventory(request):
    supplier_id = request.session.get('supplier_id')
    if not supplier_id:
        return redirect('login')

    items = database_api.get_supplier_inventory(supplier_id)
    return render(request, 'supplier_inventory_page.html', {
        'items': items
    })

def safe_int(value, default=0):
    
    try:
        return int(value)
    
    except (ValueError, TypeError):
        return default


def home(request):
    return render(request, "index.html")

def login(request):

     if request.method == 'POST':
        user_type = request.POST['user_type']
        username = request.POST['username']
        password = request.POST['password']

        print(f"Login attempt: type={user_type}, username={username}, password={password}")


        if user_type == 'customer':
            user = database_api.get_customer_by_email(username, password)
            
            if user:
                request.session['customer_id'] = user[0]
                request.session['customer_name'] = user[2]
                request.session['user_type'] = 'customer'
                return redirect('home')

        elif user_type == 'manufacturer':
            user = database_api.get_manufacturer_by_name(username, password)
            
            if user:
                request.session['manufacturer_id'] = user[0]
                request.session['manufacturer_name'] = user[1]
                request.session['user_type'] = 'manufacturer'
                return redirect('home')

        elif user_type == 'supplier':
            user = database_api.get_supplier_by_name(username, password)
            
            if user:
                request.session['supplier_id'] = user[0]
                request.session['supplier_name'] = user[1]
                request.session['user_type'] = 'supplier'
                return redirect('home')

        return render(request, 'customer_login.html', {'error': 'Invalid credentials.'})
     
     return render(request, 'customer_login.html')


def register(request):

    if request.method == 'POST':
        success = database_api.add_customer(
            request.POST['email'],          # email
            request.POST['first_name'],     # first_name
            request.POST['last_name'],      # last_name
            request.POST['street'],         # street
            request.POST['city'],           # city
            request.POST['province'],       # province
            request.POST['postal_code'],    # postal_code
            request.POST['country'],        # country
            request.POST['phone'],          # phone
            request.POST['password']        # password
        )

        if success:
            return redirect('login')
        else:
            return render(request, 'customer_registeration.html', {
                'error': 'Customer with this email already exists.'
            })

    return render(request, 'customer_registeration.html')
    

def logout(request):
    request.session.flush()
    return redirect('home')



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
    
    supplier_id = request.session.get('supplier_id')
    
    if not supplier_id:
        return redirect('login')

    items = database_api.get_supplier_inventory(supplier_id)
    
    return render(request, 'supplier_inventory_page.html', {
        'items': items
    })


def supplier_search_page(request):
    supplier_id = request.session.get('supplier_id')
    if not supplier_id:
        return redirect('login')

    selected_type = request.GET.get('type', '')
    selected_manufacturer = request.GET.get('manufacturer', '')

    components = database_api.get_all_components(selected_type, selected_manufacturer, supplier_id)
    manufacturers = database_api.get_manufacturers()

    return render(request, 'supplier_search_page.html', {
        'components': components,
        'manufacturers': manufacturers,
        'selected_type': selected_type,
        'selected_manufacturer': selected_manufacturer,
    })

def supplier_add_item(request):
    
    if request.method == 'POST':
        
        supplier_id = request.session.get('supplier_id')
        
        if not supplier_id:
            return redirect('login')

        list_part_id = int(request.POST.get('list_part_id', 0))
        result = database_api.add_store_item(list_part_id, supplier_id, 0.00)
        return redirect('supplier_inventory')

    return redirect('supplier_search_page')

@csrf_exempt
def supplier_update_item(request):
    if request.method == 'POST':
        supplier_id = request.session.get('supplier_id')
        if not supplier_id:
            return JsonResponse({'error': 'Not logged in'}, status=401)

        try:
            data = json.loads(request.body)
            item_number = data.get('item_number')
            price = data.get('price')
            units_sold = data.get('units_sold', 0)
            availability = data.get('availability', 'In stock')

            result = database_api.update_store_item(
                int(item_number), float(price),
                int(units_sold), availability
            )
            return JsonResponse({'success': result})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)




def manufacturer(request):
    manufacturer_id = request.session.get('manufacturer_id')

    if not manufacturer_id:
        return redirect('login')

    if request.method == 'POST':
       
        component_type = request.POST.get('component_type', '')
        product_name = request.POST.get('product_name', '')

        try:
            
            print(f"POST data: {dict(request.POST)}")
        
        except Exception as e:
            print(f"Error printing POST data: {e}")



        success = False

        if component_type == 'cpu':
            success = database_api.add_cpu(
                manufacturer_id, product_name,
                request.POST['chip_family'], request.POST['series'],
                 safe_int(request.POST['tdp']),  safe_int(request.POST['base_clock']),
                 safe_int(request.POST['boost_clock']),  safe_int(request.POST['l1_cache']),
                 safe_int(request.POST['l2_cache']),  safe_int(request.POST['l3_cache']),
                 safe_int(request.POST['num_cores']),  safe_int(request.POST['num_threads']),
                request.POST['architecture'], request.POST['socket_type'],
                 safe_int(request.POST['ram_type'])
            )

        elif component_type == 'gpu':
            success = database_api.add_gpu(
                manufacturer_id, product_name,
                request.POST['series'], request.POST['architecture'],
                 safe_int(request.POST['base_clock']),  safe_int(request.POST['boost_clock']),
                 safe_int(request.POST['memory_size']),  safe_int(request.POST['memory_type']),
                 safe_int(request.POST['num_cores']),  safe_int(request.POST['power_consumption']),
                 safe_int(request.POST['pci_type_id'])
            )

        elif component_type == 'motherboard':
            success = database_api.add_motherboard(
                manufacturer_id, product_name,
                 safe_int(request.POST['num_ram_slots']), request.POST['chipset_name'],
                 safe_int(request.POST['num_sata_connectors']),  safe_int(request.POST['num_cooler_headers']),
                 safe_int(request.POST['num_fan_headers']), request.POST['form_factor'],
                request.POST['socket_type'],  safe_int(request.POST['ram_type']),
                request.POST.get('has_ethernet', None),
                [],  # io_ports
                []   # pci_slots
            )

        elif component_type == 'ram':
            success = database_api.add_ram(
                manufacturer_id, product_name,
                 safe_int(request.POST['capacity']),  safe_int(request.POST['max_freq']),
                 safe_int(request.POST['ram_type'])
            )

        elif component_type == 'storage':
            storage_type = request.POST.get('storage_type', '')
            if storage_type == 'm2':
                success = database_api.add_m2_storage(
                    manufacturer_id, product_name,
                     safe_int(request.POST['capacity']),  safe_int(request.POST['read_speed']),
                     safe_int(request.POST['write_speed']), request.POST['form_factor'],
                    request.POST['pci_type_id']
                )
            elif storage_type == 'sata':
                success = database_api.add_sata_storage(
                    manufacturer_id, product_name,
                     safe_int(request.POST['capacity']),  safe_int(request.POST['read_speed']),
                     safe_int(request.POST['write_speed']), request.POST['form_factor'],
                    request.POST['interface']
                )
            elif storage_type == 'hhd':
                success = database_api.add_hhd_storage(
                    manufacturer_id, product_name,
                     safe_int(request.POST['capacity']),  safe_int(request.POST['read_speed']),
                     safe_int(request.POST['write_speed']), request.POST['form_factor'],
                    request.POST['interface']
                )

        elif component_type == 'psu':
            success = database_api.add_psu(
                manufacturer_id, product_name,
                 safe_int(request.POST['power_rating']),  safe_int(request.POST['modular']),
                 safe_int(request.POST['length_mm']),
                []  # connectors
            )

        elif component_type == 'case':
            success = database_api.add_case(
                manufacturer_id, product_name,
                 safe_int(request.POST['height']),  safe_int(request.POST['width']),
                 safe_int(request.POST['len_case']), request.POST['material'],
                 safe_int(request.POST['num_35_bays']),  safe_int(request.POST['num_25_bays']),
                 safe_int(request.POST['max_gpu_len_mm']),  safe_int(request.POST['max_psu_len_mm']),
                 safe_int(request.POST['max_air_cooler_height']),
                [],  # radiator_spaces
                [],  # io_ports
                [],  # fans
                []   # form_factors
            )

        elif component_type == 'cpu-cooler':
            cooler_type = request.POST.get('cooler_type', '')
            if cooler_type == 'air':
                success = database_api.add_air_cooler(
                    manufacturer_id, product_name,
                     safe_int(request.POST['noise_level']),
                     safe_int(request.POST['air_fan_rpm']),
                     safe_int(request.POST['air_height'])
                )
            elif cooler_type == 'liquid':
                success = database_api.add_liquid_cooler(
                    manufacturer_id, product_name,
                     safe_int(request.POST['noise_level']),
                     safe_int(request.POST['num_fans']),  safe_int(request.POST['len_cool']),
                     safe_int(request.POST['liquid_width']),  safe_int(request.POST['liquid_height']),
                     safe_int(request.POST['liquid_fan_rpm']),
                     safe_int(request.POST['cooling_tube_length'])
                )

        elif component_type == 'fan':
            success = database_api.add_fan(
                manufacturer_id, product_name,
                 safe_int(request.POST['fan_rpm']), float(request.POST['noise_level']),
                 safe_int(request.POST['size_category_mm'])
            )

        elif component_type == 'ethernet-controller':
            eth_name = request.POST.get('eth_product_name', product_name)
            success = database_api.add_ethernet_controller(
                manufacturer_id, eth_name
            )

        elif component_type == 'wifi-module':
            wifi_name = request.POST.get('wifi_product_name', product_name)
            success = database_api.add_wifi_module(
                manufacturer_id, wifi_name,
                 safe_int(request.POST['wifi_pci_type_id']),
                 safe_int(request.POST['wifi_pin_count'])
            )

        if success:
            return redirect('view_my_components')
        else:
            return render(request, 'manufacturer_selection_page.html', {
                'error': 'Failed to add component. Please try again.'
            })

    return render(request, 'manufacturer_selection_page.html')

def view_my_components(request):
    manufacturer_id = request.session.get('manufacturer_id')
    print(f"Manufacturer ID from session: {manufacturer_id}")

    if not manufacturer_id:
        return redirect('login')
    

    try:
        components = database_api.get_components_by_manufacturer(manufacturer_id)
        print(f"Components found: {components}")
    except Exception as e:
        print(f"Error: {e}")
        components = []

    components = database_api.get_components_by_manufacturer(manufacturer_id)
    return render(request, 'manufacturer_components.html', {
        'components': components
    })


def delete_component(request, part_id):
    if request.method == 'POST':
        database_api.delete_component(part_id)
    return redirect('view_my_components')