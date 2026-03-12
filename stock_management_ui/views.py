from contextlib import nullcontext

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from stock_management_ui.models import Branches, InventoryItems, Products, Sales, SaleProducts, ItemStock, ProductIngredients
from stock_management_ui.forms import BranchesForm, InventoryItemsForm, ProductsForm, SalesForm, SaleProductsForm, ItemStockForm, ProductIngredientsForm
from stock_management_ui.tests import can_access_sales
from stock_management_ui.navbar_fields import get_navbar_fields

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Validate the login credentials
        is_valid_user = authenticate(request, username=username, password=password)
        if is_valid_user is not None:
            #Login the user
            login(request,is_valid_user)

            #Redirect the user to the corresponding webpage for their account group
            try:
                group = request.user.groups.all()[0]
                if group.name == "baker":
                    return HttpResponseRedirect('/baker_home')
                if group.name == "manager":
                    return HttpResponseRedirect('/manager_home')
                if group.name == "shop assistant":
                    return HttpResponseRedirect('/shop_assistant_home')
                if group.name == "till":
                    return HttpResponseRedirect('/manage_sales')
            except IndexError:
                print("User account has no group")

        else:
            info={
                'Invalid_login_error': 'Invalid login details. Try again.'
            }
            return render(request,"login.html", {'info': info})

    return render(request, 'login.html')

@login_required(login_url="/login/")
def baker_home(request):
    navbar_info = get_navbar_fields(request)
    info = {
        'navbar_info': navbar_info,
    }
    return render(request, 'baker_home.html', {'info': info})

@login_required(login_url="/login/")
def manager_home(request):
    navbar_info = get_navbar_fields(request)
    info = {
        'navbar_info': navbar_info,
    }
    return render(request, 'manager_home.html', {'info': info})

@login_required(login_url="/login/")
def shop_assistant_home(request):
    navbar_info = get_navbar_fields(request)
    info = {
        'navbar_info': navbar_info,
    }
    return render(request, 'shop_assistant_home.html', {'info': info})

@login_required(login_url="/login/")
@permission_required('stock_management_ui.view_branches')
def manage_branches(request):

    #PREPARING DATA TO SEND TO THE WEBPAGE

    branch = Branches.objects.get(branch_id=1)
    unfiltered_fields = branch._meta.get_fields()
    data = Branches.objects.all()

    #Filter fields to names which are formated to be easily readable
    readable_fields = [field.verbose_name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "is_deleted"]

    #Filter fields to their plain names (Used for form input name attribute)
    unformatted_field_names = [field.name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "branch_id" and field.name != "is_deleted"]

    #Extract the field values from the gathered data
    branch_fields = ["branch_id", "branch_name", "branch_phone_number", "branch_city"]
    field_values = []
    for record in data:
        if getattr(record, 'is_deleted') == False:
            filtered_fields = [getattr(record, field) for field in branch_fields]
            field_values.append(filtered_fields)

    navbar_info = get_navbar_fields(request)



    #CRUD MANAGEMENT

    row_editing_data = None
    #Displays error to user if CRUD operation fails
    crud_error = ""
    if request.method == "POST":
        #Handles requests to add row to database
        if 'create_row' in request.POST:
            create_form = BranchesForm(request.POST)
            if create_form.is_valid():
                create_form.save()
                return HttpResponseRedirect('/manage_branches')
            else:
                crud_error = create_form.errors

        #Handles record deletion requests
        elif 'delete_row' in request.POST:
            button_pressed = request.POST.get('delete_row')

            branch = Branches.objects.get(branch_id=button_pressed)
            branch.is_deleted = True
            branch.save()
            return HttpResponseRedirect('/manage_branches')

        #Handles record edit requests once the user submits the edit
        elif 'submit_edit_row' in request.POST:
            button_pressed = request.POST.get('submit_edit_row')
            branch = Branches.objects.get(branch_id=button_pressed)
            edited_branch = BranchesForm(request.POST, instance=branch)
            if edited_branch.is_valid():
                edited_branch.save()
                # Reload page with new values
                return HttpResponseRedirect('/manage_branches')
            else:
                crud_error = edited_branch.errors


        #Handles record edit requests before the edit is submitted
        elif 'edit_row' in request.POST:
            button_pressed = request.POST.get('edit_row')
            branch = Branches.objects.get(branch_id=button_pressed)
            row_editing_data = BranchesForm(instance=branch)

            info = {
                'branch': branch,
                'fields': readable_fields,
                'field_values': field_values,
                'unformatted_field_names': unformatted_field_names,
                'crud_error': crud_error,
                'row_editing_data': row_editing_data,
                'inheriting_page_add_row_permission': 'stock_management_ui.add_branches',
                'navbar_info': navbar_info,
            }

            return render(request, 'manage_branches.html', {'info': info})

    info = {
        'branch': branch,
        'fields': readable_fields,
        'field_values': field_values,
        'unformatted_field_names': unformatted_field_names,
        'crud_error': crud_error,
        'row_editing_data': row_editing_data,
        'inheriting_page_add_row_permission': 'stock_management_ui.add_branches',
        'navbar_info': navbar_info,
    }
    return render(request, 'manage_branches.html', {'info': info})

@login_required(login_url="/login/")
@permission_required('stock_management_ui.view_inventoryitems')
def manage_item_types(request):

    #PREPARING DATA TO SEND TO THE WEBPAGE

    item_type = InventoryItems.objects.get(item_id=1)
    unfiltered_fields = item_type._meta.get_fields()
    data = InventoryItems.objects.all()

    #Filter fields to names which are formated to be easily readable
    readable_fields = [field.verbose_name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "is_deleted"]

    #Filter fields to their plain names (Used for form input name attribute)
    unformatted_field_names = [field.name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "item_id" and field.name != "is_deleted"]

    #Extract the field values from the gathered data
    inventory_item_fields = ["item_id", "item_name", "item_cost", "item_category", "is_deleted"]
    product_fields = ["product_category", "product_price", "product_shelf_life_seconds"]
    field_values = []
    filtered_fields = []
    #Used later to indicate if there is a corresponding Products record
    for record in data:
        if getattr(record, 'is_deleted') == False:
            filtered_fields = [getattr(record, field) for field in inventory_item_fields if field != "is_deleted"]
            if getattr(record, 'item_category') == 'Product':
                try:
                    product_object = Products.objects.get(item_id=record.item_id)
                    filtered_product_fields = [getattr(product_object, field) for field in product_fields if field != "is_deleted" and field != "item_id"]
                    filtered_fields.extend(filtered_product_fields)

                except Products.DoesNotExist:
                    pass
        field_values.append(filtered_fields)

    navbar_info = get_navbar_fields(request)

    #CRUD MANAGEMENT

    item_type_row_editing_data = None
    product_row_editing_data = None
    #Displays error to user if CRUD operation fails
    crud_error = ""
    if request.method == "POST":
        #Handles requests to add row to database
        if 'create_row' in request.POST:
            create_form = InventoryItemsForm(request.POST)
            if create_form.is_valid():
                create_form.save()
                return HttpResponseRedirect('/manage_item_types')
            else:
                crud_error = create_form.errors

        #Handles record deletion requests
        elif 'delete_row' in request.POST:
            button_pressed = request.POST.get('delete_row')

            item_type = InventoryItems.objects.get(item_id=button_pressed)
            item_type.is_deleted = True
            item_type.save()
            return HttpResponseRedirect('/manage_item_types')

        #Handles record edit requests once the user submits the edit
        elif 'submit_edit_row' in request.POST:
            button_pressed = request.POST.get('submit_edit_row')
            item_type = InventoryItems.objects.get(item_id=button_pressed)
            edited_item_type = InventoryItemsForm(request.POST, instance=item_type)

            if edited_item_type.is_valid():
                edited_item_type.save()

                #If there is also product data to edit
                if item_type.item_category == 'Product':
                    product = Products.objects.get(item_id=button_pressed)
                    edited_product = ProductsForm(request.POST, instance=product)
                    if edited_product.is_valid():
                        edited_product.save()
                    else:
                        crud_error = edited_product.errors
                        print(crud_error)
                #Reload page with new values
                return HttpResponseRedirect('/manage_item_types')

            else:
                crud_error = edited_item_type.errors


        #Handles record edit requests before the edit is submitted
        elif 'edit_row' in request.POST:
            button_pressed = request.POST.get('edit_row')
            item_type = InventoryItems.objects.get(item_id=button_pressed)
            item_type_row_editing_data = InventoryItemsForm(instance=item_type)
            try:
                product = Products.objects.get(item_id=button_pressed)
                product_row_editing_data = ProductsForm(instance=product)
            except Products.DoesNotExist:
                pass

            info = {
                'item_type': item_type,
                'fields': readable_fields,
                'field_values': field_values,
                'unformatted_field_names': unformatted_field_names,
                'crud_error': crud_error,
                'row_editing_data': item_type_row_editing_data,
                'product_row_editing_data': product_row_editing_data,
                'aditional_fields': product_fields,
                'inheriting_page_add_row_permission': 'stock_management_ui.add_inventoryitems',
                'navbar_info': navbar_info,
            }

            return render(request, 'manage_item_types.html', {'info': info})

    info = {
        'item_type': item_type,
        'fields': readable_fields,
        'field_values': field_values,
        'unformatted_field_names': unformatted_field_names,
        'crud_error': crud_error,
        'row_editing_data': item_type_row_editing_data,
        'product_row_editing_data': product_row_editing_data,
        'aditional_fields': product_fields,
        'inheriting_page_add_row_permission': 'stock_management_ui.add_inventoryitems',
        'navbar_info': navbar_info,
    }
    return render(request, 'manage_item_types.html', {'info': info})

@login_required(login_url="/login/")
@permission_required('stock_management_ui.view_itemstock')
def manage_stock(request):

    #PREPARING DATA TO SEND TO THE WEBPAGE

    stock = ItemStock.objects.get(stock_id=1)
    unfiltered_fields = stock._meta.get_fields()
    data = ItemStock.objects.all()

    #Filter fields to names which are formated to be easily readable
    readable_fields = [field.verbose_name for field in unfiltered_fields if hasattr(field, 'verbose_name')]

    #Filter fields to their plain names (Used for form input name attribute)
    unformatted_field_names = [field.name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "stock_id"]

    #Extract the field values from the gathered data
    stock_fields = ["stock_id", "item_id", "branch", "item_quantity"]
    field_values = []
    for record in data:
        filtered_fields = [getattr(record, field) if field != "item_id" and field != "branch" else record.item_id_id if field == "item_id" else record.branch_id if field == "branch" else None for field in stock_fields]
        field_values.append(filtered_fields)

    navbar_info = get_navbar_fields(request)



    #CRUD MANAGEMENT

    row_editing_data = None
    #Displays error to user if CRUD operation fails
    crud_error = ""
    if request.method == "POST":
        #Handles requests to add row to database
        if 'create_row' in request.POST:
            create_form = ItemStockForm(request.POST)
            if create_form.is_valid():
                create_form.save()
                return HttpResponseRedirect('/manage_stock')
            else:
                crud_error = create_form.errors

        #Handles record deletion requests
        elif 'delete_row' in request.POST:
            button_pressed = request.POST.get('delete_row')

            stock = ItemStock.objects.get(stock_id=button_pressed)
            stock.is_deleted = True
            stock.save()
            return HttpResponseRedirect('/manage_stock')

        #Handles record edit requests once the user submits the edit
        elif 'submit_edit_row' in request.POST:
            button_pressed = request.POST.get('submit_edit_row')
            stock = ItemStock.objects.get(stock_id=button_pressed)
            edited_stock = ItemStockForm(request.POST, instance=stock)
            if edited_stock.is_valid():
                edited_stock.save()
                # Reload page with new values
                return HttpResponseRedirect('/manage_stock')
            else:
                crud_error = edited_stock.errors


        #Handles record edit requests before the edit is submitted
        elif 'edit_row' in request.POST:
            button_pressed = request.POST.get('edit_row')
            stock = ItemStock.objects.get(stock_id=button_pressed)
            row_editing_data = ItemStockForm(instance=stock)

            info = {
                'stock': stock,
                'fields': readable_fields,
                'field_values': field_values,
                'unformatted_field_names': unformatted_field_names,
                'crud_error': crud_error,
                'row_editing_data': row_editing_data,
                'inheriting_page_add_row_permission': 'stock_management_ui.add_itemstock',
                'navbar_info': navbar_info,
            }

            return render(request, 'manage_stock.html', {'info': info})

    info = {
        'branch': stock,
        'fields': readable_fields,
        'field_values': field_values,
        'unformatted_field_names': unformatted_field_names,
        'crud_error': crud_error,
        'row_editing_data': row_editing_data,
        'inheriting_page_add_row_permission': 'stock_management_ui.add_itemstock',
        'navbar_info': navbar_info,
    }
    return render(request, 'manage_stock.html', {'info': info})

@login_required(login_url="/login/")
@user_passes_test(can_access_sales)
def manage_sales(request):

    #PREPARING DATA TO SEND TO THE WEBPAGE

    sale = Sales.objects.get(sale_id=1)
    unfiltered_fields = sale._meta.get_fields()
    data = Sales.objects.all()

    #Filter fields to names which are formated to be easily readable
    readable_fields = [field.verbose_name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "is_deleted"]

    #Filter fields to their plain names (Used for form input name attribute)
    unformatted_field_names = [field.name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "sale_id" and field.name != "is_deleted"]

    #Extract the field values from the gathered data
    sale_fields = ["sale_id", "branch_id", "sale_date_time", "is_card_payment", "is_deleted"]
    field_values = []
    for record in data:
        if getattr(record, 'is_deleted') == False:
            filtered_fields = [getattr(record, field) if field != "branch_id" else record.branch_id_id if field == "branch_id" else None for field in sale_fields]
            field_values.append(filtered_fields)

    navbar_info = get_navbar_fields(request)



    #CRUD MANAGEMENT

    row_editing_data = None
    #Displays error to user if CRUD operation fails
    crud_error = ""
    if request.method == "POST":
        #Handles requests to add row to database
        if 'create_row' in request.POST:
            create_form = SalesForm(request.POST)
            if create_form.is_valid():
                create_form.save()
                return HttpResponseRedirect('/manage_sales')
            else:
                crud_error = create_form.errors

        #Handles record deletion requests
        elif 'delete_row' in request.POST:
            button_pressed = request.POST.get('delete_row')

            sale = Sales.objects.get(sale_id=button_pressed)
            sale.is_deleted = True
            sale.save()
            return HttpResponseRedirect('/manage_sales')

        #Handles record edit requests once the user submits the edit
        elif 'submit_edit_row' in request.POST:
            button_pressed = request.POST.get('submit_edit_row')
            sale = Sales.objects.get(sale_id=button_pressed)
            edited_sale = SalesForm(request.POST, instance=sale)
            if edited_sale.is_valid():
                edited_sale.save()
                # Reload page with new values
                return HttpResponseRedirect('/manage_sales')
            else:
                crud_error = edited_sale.errors


        #Handles record edit requests before the edit is submitted
        elif 'edit_row' in request.POST:
            button_pressed = request.POST.get('edit_row')
            sale = Sales.objects.get(sale_id=button_pressed)
            row_editing_data = SalesForm(instance=sale)

            info = {
                'sale': sale,
                'fields': readable_fields,
                'field_values': field_values,
                'unformatted_field_names': unformatted_field_names,
                'crud_error': crud_error,
                'row_editing_data': row_editing_data,
                'inheriting_page_add_row_permission': 'stock_management_ui.add_sales',
                'navbar_info': navbar_info,
            }

            return render(request, 'manage_sales.html', {'info': info})

    info = {
        'sale': sale,
        'fields': readable_fields,
        'field_values': field_values,
        'unformatted_field_names': unformatted_field_names,
        'crud_error': crud_error,
        'row_editing_data': row_editing_data,
        'inheriting_page_add_row_permission': 'stock_management_ui.add_sales',
        'navbar_info': navbar_info,
    }
    return render(request, 'manage_sales.html', {'info': info})

@login_required(login_url="/login/")
@user_passes_test(can_access_sales)
def manage_sale_products(request):

    #PREPARING DATA TO SEND TO THE WEBPAGE

    sale_product = SaleProducts.objects.get(sale_id=1, product_id=16)
    unfiltered_fields = sale_product._meta.get_fields()
    data = SaleProducts.objects.all()

    #Filter fields to names which are formated to be easily readable
    readable_fields = [field.verbose_name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "is_deleted" and field.name != "pk"]

    #Filter fields to their plain names (Used for form input name attribute)
    unformatted_field_names = [field.name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "is_deleted" and field.name != "pk"]

    #Extract the field values from the gathered data
    sale_product_fields = ["sale_id", "product_id", "product_quantity"]
    field_values = []
    for record in data:
        if getattr(record, 'is_deleted') == False:
            filtered_fields = [getattr(record, field) if field == "product_quantity" else record.sale_id_id if field == "sale_id" else record.product_id_id if field == "product_id" else None for field in sale_product_fields]
            field_values.append(filtered_fields)

    navbar_info = get_navbar_fields(request)



    #CRUD MANAGEMENT

    row_editing_data = None
    #Displays error to user if CRUD operation fails
    crud_error = ""
    if request.method == "POST":
        #Handles requests to add row to database
        if 'create_row' in request.POST:
            create_form = SaleProductsForm(request.POST)
            if create_form.is_valid():
                create_form.save()
                return HttpResponseRedirect('/manage_sale_products')
            else:
                crud_error = create_form.errors

        #Handles record deletion requests
        elif 'delete_row' in request.POST:
            button_pressed = request.POST.get('delete_row')
            #Split the returned value into a list of composite key fields
            composite_key = button_pressed.split("|||")
            sale_product = SaleProducts.objects.get(sale_id=composite_key[0], product_id=composite_key[1])
            sale_product.is_deleted = True
            sale_product.save()
            return HttpResponseRedirect('/manage_sale_products')

        #Handles record edit requests once the user submits the edit
        elif 'submit_edit_row' in request.POST:
            button_pressed = request.POST.get('submit_edit_row')
            # Split the returned value into a list of composite key fields
            composite_key = button_pressed.split("|||")
            sale_product = SaleProducts.objects.get(sale_id=composite_key[0], product_id=composite_key[1])
            edited_sale_product = SaleProductsForm(request.POST, instance=sale_product)
            if edited_sale_product.is_valid():
                edited_sale_product.save()
                # Reload page with new values
                return HttpResponseRedirect('/manage_sale_products')
            else:
                crud_error = edited_sale_product.errors


        #Handles record edit requests before the edit is submitted
        elif 'edit_row' in request.POST:
            button_pressed = request.POST.get('edit_row')
            #Split the returned value into a list of composite key fields
            composite_key = button_pressed.split("|||")
            sale_product = SaleProducts.objects.get(sale_id=composite_key[0], product_id=composite_key[1])
            row_editing_data = SaleProductsForm(instance=sale_product)


            info = {
                'sale_product': sale_product,
                'fields': readable_fields,
                'field_values': field_values,
                'unformatted_field_names': unformatted_field_names,
                'crud_error': crud_error,
                'row_editing_data': row_editing_data,
                'inheriting_page_add_row_permission': 'stock_management_ui.add_saleproducts',
                'navbar_info': navbar_info,
            }

            return render(request, 'manage_sale_products.html', {'info': info})

    info = {
        'sale_product': sale_product,
        'fields': readable_fields,
        'field_values': field_values,
        'unformatted_field_names': unformatted_field_names,
        'crud_error': crud_error,
        'row_editing_data': row_editing_data,
        'inheriting_page_add_row_permission': 'stock_management_ui.add_saleproducts',
        'navbar_info': navbar_info,
    }
    return render(request, 'manage_sale_products.html', {'info': info})

@login_required(login_url="/login/")
@permission_required('stock_management_ui.view_productingredients')
def manage_product_ingredients(request):

    #PREPARING DATA TO SEND TO THE WEBPAGE

    product_ingredient = ProductIngredients.objects.get(product_id=7, ingredient_id=107)
    unfiltered_fields = product_ingredient._meta.get_fields()
    data = ProductIngredients.objects.all()

    #Filter fields to names which are formated to be easily readable
    readable_fields = [field.verbose_name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "pk"]

    #Filter fields to their plain names (Used for form input name attribute)
    unformatted_field_names = [field.name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "pk"]

    #Extract the field values from the gathered data
    product_ingredient_fields = ["product_id", "ingredient_id", "ingredient_quantity"]
    field_values = []
    for record in data:
        filtered_fields = [getattr(record, field) if field == "ingredient_quantity" else record.product_id_id if field == "product_id" else record.ingredient_id_id if field == "ingredient_id" else None for field in product_ingredient_fields]
        field_values.append(filtered_fields)

    navbar_info = get_navbar_fields(request)



    #CRUD MANAGEMENT

    row_editing_data = None
    #Displays error to user if CRUD operation fails
    crud_error = ""
    if request.method == "POST":
        #Handles requests to add row to database
        if 'create_row' in request.POST:
            create_form = ProductIngredientsForm(request.POST)
            if create_form.is_valid():
                create_form.save()
                return HttpResponseRedirect('/manage_product_ingredients')
            else:
                crud_error = create_form.errors

        #Handles record deletion requests
        elif 'delete_row' in request.POST:
            button_pressed = request.POST.get('delete_row')
            #Split the returned value into a list of composite key fields
            composite_key = button_pressed.split("|||")
            product_ingredient = ProductIngredients.objects.get(product_id=composite_key[0], ingredient_id=composite_key[1])
            product_ingredient.delete()
            return HttpResponseRedirect('/manage_product_ingredients')

        #Handles record edit requests once the user submits the edit
        elif 'submit_edit_row' in request.POST:
            button_pressed = request.POST.get('submit_edit_row')
            # Split the returned value into a list of composite key fields
            composite_key = button_pressed.split("|||")
            product_ingredient = ProductIngredients.objects.get(product_id=composite_key[0], ingredient_id=composite_key[1])
            edited_product_ingredient = ProductIngredientsForm(request.POST, instance=product_ingredient)
            if edited_product_ingredient.is_valid():
                edited_product_ingredient.save()
                # Reload page with new values
                return HttpResponseRedirect('/manage_product_ingredients')
            else:
                crud_error = edited_product_ingredient.errors


        #Handles record edit requests before the edit is submitted
        elif 'edit_row' in request.POST:
            button_pressed = request.POST.get('edit_row')
            #Split the returned value into a list of composite key fields
            composite_key = button_pressed.split("|||")
            product_ingredient = ProductIngredients.objects.get(product_id=composite_key[0], ingredient_id=composite_key[1])
            row_editing_data = ProductIngredientsForm(instance=product_ingredient)


            info = {
                'product_ingredient': product_ingredient,
                'fields': readable_fields,
                'field_values': field_values,
                'unformatted_field_names': unformatted_field_names,
                'crud_error': crud_error,
                'row_editing_data': row_editing_data,
                'inheriting_page_add_row_permission': 'stock_management_ui.add_productingredients',
                'navbar_info': navbar_info,
            }

            return render(request, 'manage_product_ingredients.html', {'info': info})

    info = {
        'product_ingredient': product_ingredient,
        'fields': readable_fields,
        'field_values': field_values,
        'unformatted_field_names': unformatted_field_names,
        'crud_error': crud_error,
        'row_editing_data': row_editing_data,
        'inheriting_page_add_row_permission': 'stock_management_ui.add_productingredients',
        'navbar_info': navbar_info,
    }
    return render(request, 'manage_product_ingredients.html', {'info': info})