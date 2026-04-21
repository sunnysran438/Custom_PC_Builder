def user_context(request):

    customer_id = request.session.get('customer_id')
    account_status = None
    
    if customer_id:
        from pc_builder_app import database_api
        customer = database_api.get_customer_by_id(customer_id)
        if customer and len(customer) > 11:
            account_status = customer[11]



    return {
        'user_type': request.session.get('user_type', None),
        'customer_name': request.session.get('customer_name', None),
        'manufacturer_name': request.session.get('manufacturer_name', None),
        'supplier_name': request.session.get('supplier_name', None),
        'account_status': account_status,

    }