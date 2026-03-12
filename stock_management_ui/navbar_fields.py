def get_navbar_fields(request):
    navbar_info = []
    try:
        group = request.user.groups.all()[0]
        if group.name == "baker":
            pass
            navbar_info = [
                {"url": "/manage_stock", "name": "Manage Stock"},
                {"url": "/manage_product_ingredients", "name": "Manage Product Ingredients"},
                ]

        if group.name == "shop assistant":
            navbar_info = [
                {"url": "/manage_stock", "name": "Manage Stock"},
                {"url": "/manage_item_types", "name": "Manage Item Types"},
                {"url": "/manage_sales", "name": "Manage Sales"},
                {"url": "/manage_sale_products", "name": "Manage Sale Products"},
            ]

        if group.name == "manager":
            navbar_info = [
                {"url": "/manage_stock", "name": "Manage Stock"},
                {"url": "/manage_item_types", "name": "Manage Item Types"},
                {"url": "/manage_product_ingredients", "name": "Manage Product Ingredients"},
                {"url": "/manage_branches", "name": "Manage Branches"},
                {"url": "/manage_sales", "name": "Manage Sales"},
                {"url": "/manage_sale_products", "name": "Manage Sale Products"},
            ]
        if group.name == "till":
            navbar_info = [
                {"url": "/manage_sales", "name": "Manage Sales"},
                {"url": "/manage_sale_products", "name": "Manage Sale Products"},
            ]

    except IndexError:
        print("Could not find group for user account")
    return navbar_info