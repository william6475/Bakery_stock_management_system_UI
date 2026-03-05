from django.shortcuts import render
from stock_management_ui.models import Branches, Deliveries, InventoryItems, DeliveryItems, Products, Sales, SaleProducts, ItemStock, ProductIngredients
def login(request):
    return render(request, 'login.html')

def manage_table_base_template(request):
    branch = Branches.objects.get(branch_id=1)
    unfiltered_fields = branch._meta.get_fields()
    data = Branches.objects.all()

    #Filters out fields which are not directly part of the model
    fields = [field.verbose_name for field in unfiltered_fields if hasattr(field, 'verbose_name') and field.name != "is_deleted"]

    #Exxtract the field values from the gathered data
    branch_fields = ["branch_id", "branch_name", "branch_phone_number", "branch_city"]
    field_values = []
    for record in data:
        filtered_fields = [getattr(record, field) for field in branch_fields]
        field_values.append(filtered_fields)


    info = {
        'branch': branch,
        'fields': fields,
        'field_values': field_values,
    }
    return render(request, 'base_templates/manage_table_base_template.html', {'info': info})