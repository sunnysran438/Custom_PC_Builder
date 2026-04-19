def user_context(request):
    return {
        'user_type': request.session.get('user_type', None),
        'customer_name': request.session.get('customer_name', None),
        'manufacturer_name': request.session.get('manufacturer_name', None),
        'supplier_name': request.session.get('supplier_name', None),
    }