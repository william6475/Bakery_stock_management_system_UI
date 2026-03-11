from.models import *
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@receiver(post_migrate)
def group_permission_asignment(sender, **kwargs):

    #Prevent this code from running if a migration is happening to a different app
    if sender.name != 'stock_management_ui':
        return

    #Ensure the user groups already exist
    baker, useless = Group.objects.get_or_create(name="baker")
    manager, useless = Group.objects.get_or_create(name="manager")
    shop_assistant, useless = Group.objects.get_or_create(name="shop assistant")
    till, useless = Group.objects.get_or_create(name="till")

    branches = ContentType.objects.get_for_model(Branches)
    inventoryitems = ContentType.objects.get_for_model(InventoryItems)
    products = ContentType.objects.get_for_model(Products)
    sales = ContentType.objects.get_for_model(Sales)
    saleproducts = ContentType.objects.get_for_model(SaleProducts)
    itemstock = ContentType.objects.get_for_model(ItemStock)
    productingredients = ContentType.objects.get_for_model(ProductIngredients)

    #Get the default Django permissions created for each model (view, add, delete, change)
    can_view_branches, useless = Permission.objects.get_or_create(codename="view_branches", content_type=branches)
    can_add_branches, useless = Permission.objects.get_or_create(codename="add_branches", content_type=branches)
    can_delete_branches, useless = Permission.objects.get_or_create(codename="delete_branches", content_type=branches)
    can_change_branches, useless = Permission.objects.get_or_create(codename="change_branches", content_type=branches)

    can_view_inventoryitems, useless = Permission.objects.get_or_create(codename="view_inventoryitems", content_type=inventoryitems)
    can_add_inventoryitems, useless = Permission.objects.get_or_create(codename="add_inventoryitems", content_type=inventoryitems)
    can_delete_inventoryitems, useless = Permission.objects.get_or_create(codename="delete_inventoryitems", content_type=inventoryitems)
    can_change_inventoryitems, useless = Permission.objects.get_or_create(codename="change_inventoryitems", content_type=inventoryitems)

    can_view_products, useless = Permission.objects.get_or_create(codename="view_products", content_type=products)
    can_add_products, useless = Permission.objects.get_or_create(codename="add_products", content_type=products)
    can_delete_products, useless = Permission.objects.get_or_create(codename="delete_products", content_type=products)
    can_change_products, useless = Permission.objects.get_or_create(codename="change_products", content_type=products)

    can_view_sales, useless = Permission.objects.get_or_create(codename="view_sales", content_type=sales)
    can_add_sales, useless = Permission.objects.get_or_create(codename="add_sales", content_type=sales)
    can_delete_sales, useless = Permission.objects.get_or_create(codename="delete_sales", content_type=sales)
    can_change_sales, useless = Permission.objects.get_or_create(codename="change_sales", content_type=sales)

    can_view_saleproducts, useless = Permission.objects.get_or_create(codename="view_saleproducts", content_type=saleproducts)
    can_add_saleproducts, useless = Permission.objects.get_or_create(codename="add_saleproducts", content_type=saleproducts)
    can_delete_saleproducts, useless = Permission.objects.get_or_create(codename="delete_saleproducts", content_type=saleproducts)
    can_change_saleproducts, useless = Permission.objects.get_or_create(codename="change_saleproducts", content_type=saleproducts)

    can_view_itemstock, useless = Permission.objects.get_or_create(codename="view_itemstock", content_type=itemstock)
    can_add_itemstock, useless = Permission.objects.get_or_create(codename="add_itemstock", content_type=itemstock)
    can_delete_itemstock, useless = Permission.objects.get_or_create(codename="delete_itemstock", content_type=itemstock)
    can_change_itemstock, useless = Permission.objects.get_or_create(codename="change_itemstock", content_type=itemstock)

    can_view_productingredients, useless = Permission.objects.get_or_create(codename="view_productingredients", content_type=productingredients)
    can_add_productingredients, useless = Permission.objects.get_or_create(codename="add_productingredients", content_type=productingredients)
    can_delete_productingredients, useless = Permission.objects.get_or_create(codename="delete_productingredients", content_type=productingredients)
    can_change_productingredients, useless = Permission.objects.get_or_create(codename="change_productingredients", content_type=productingredients)

    #Assign permissions to manager group
    #Branches CRUD
    manager.permissions.add(can_view_branches)
    manager.permissions.add(can_add_branches)
    manager.permissions.add(can_delete_branches)
    manager.permissions.add(can_change_branches)
    #Stock RU
    manager.permissions.add(can_view_itemstock)
    manager.permissions.add(can_change_itemstock)
    #Item types / products CRUD
    manager.permissions.add(can_view_inventoryitems)
    manager.permissions.add(can_add_inventoryitems)
    manager.permissions.add(can_delete_inventoryitems)
    manager.permissions.add(can_change_inventoryitems)
    manager.permissions.add(can_view_products)
    manager.permissions.add(can_add_products)
    manager.permissions.add(can_delete_products)
    manager.permissions.add(can_change_products)
    #Product ingredients CRUD
    manager.permissions.add(can_view_productingredients)
    manager.permissions.add(can_add_productingredients)
    manager.permissions.add(can_delete_productingredients)
    manager.permissions.add(can_change_productingredients)
    #Sales RU
    manager.permissions.add(can_view_sales)
    manager.permissions.add(can_change_sales)
    #Sale products RU
    manager.permissions.add(can_view_saleproducts)
    manager.permissions.add(can_change_saleproducts)

    #Assign permissions to baker group
    #Stock RU
    baker.permissions.add(can_view_itemstock)
    baker.permissions.add(can_change_itemstock)
    #Item types / products R
    baker.permissions.add(can_view_inventoryitems)
    baker.permissions.add(can_view_products)
    #Sales R
    baker.permissions.add(can_view_sales)
    #Sale products R
    baker.permissions.add(can_view_saleproducts)

    # Assign permissions to the shop assistant group
    #Stock RU
    shop_assistant.permissions.add(can_view_itemstock)
    shop_assistant.permissions.add(can_change_itemstock)
    #Item types / products R
    shop_assistant.permissions.add(can_view_inventoryitems)
    shop_assistant.permissions.add(can_view_products)
    #Sales R
    shop_assistant.permissions.add(can_view_sales)
    #Sale products R
    shop_assistant.permissions.add(can_view_saleproducts)

    # Assign permissions to the till group
    #Sales RU
    till.permissions.add(can_view_sales)
    till.permissions.add(can_change_sales)
    #Sale products RU
    till.permissions.add(can_view_saleproducts)
    till.permissions.add(can_change_saleproducts)