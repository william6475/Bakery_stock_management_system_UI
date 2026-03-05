from django.utils.translation import gettext_lazy as _
from django.db import models

#Accesses data for bakery chain branches
class Branches(models.Model):
    branch_id = models.SmallAutoField(db_column='Branch_ID', primary_key=True)
    branch_name = models.CharField(db_column='Branch_name', max_length=100, blank=False, null=False)
    branch_phone_number = models.CharField(db_column='Branch_phone_number', max_length=15, blank=True, null=True)
    branch_city = models.CharField(db_column='Branch_city', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Branches'

#Accesses delivery data
class Deliveries(models.Model):
    delivery_id = models.AutoField(db_column='Delivery_ID', primary_key=True)
    branch_id = models.ForeignKey(Branches, models.DO_NOTHING, db_column='Branch_ID')
    delivery_date_time = models.DateTimeField(db_column='Delivery_date_time', blank=True, null=True)
    is_delivered = models.BooleanField(db_column='Is_delivered', default = False)

    class Meta:
        managed = False
        db_table = 'Deliveries'

#Accesses the different item types which can be stored in stock
class InventoryItems(models.Model):
    class Item_category_choices(models.TextChoices):
        Product = "Product", _("Product")
        Ingredient = "Ingredient", _("Ingredient")
        Packaging = "Packaging", _("Packaging")
        Other = "Other", _("Other")
    item_id = models.SmallAutoField(db_column='Item_ID', primary_key=True)
    item_name = models.CharField(db_column='Item_name', max_length=100, blank=True, null=True)
    item_cost = models.DecimalField(db_column='Item_cost', max_digits=8, decimal_places=2, blank=True, null=True)
    item_category = models.CharField(db_column='Item_category', max_length=10, choices=Item_category_choices)
    is_deleted = models.BooleanField(db_column='Is_deleted', default = False)

    class Meta:
        managed = False
        db_table = 'Inventory_items'

#Accesses the items within deliveries
class DeliveryItems(models.Model):
    pk = models.CompositePrimaryKey('delivery_id', 'item_id')
    delivery_id = models.ForeignKey(Deliveries, models.DO_NOTHING, db_column='Delivery_ID')
    item_id = models.ForeignKey('InventoryItems', models.DO_NOTHING, db_column='Item_ID')
    item_quantity = models.PositiveSmallIntegerField(db_column='Item_quantity', null=False)

    class Meta:
        managed = False
        db_table = 'Delivery_items'

#Accesses product types
#Products are also stored as item types in the InventoryItems table
class Products(models.Model):
    #Choices for the product_category enum field
    class Product_category_choices(models.TextChoices):
        Cake = "Cake", _("Cake")
        Bread = "Bread", _("Bread")
        Pastry = "Pastry", _("Pastry")
        Other = "Other", _("Other")
    product_id = models.SmallAutoField(db_column='Product_ID', primary_key=True)
    item_id = models.ForeignKey(InventoryItems, models.DO_NOTHING, db_column='Item_ID')
    product_category = models.CharField(max_length=6, choices=Product_category_choices, blank=False, null=False)
    product_price = models.DecimalField(db_column='Product_price', max_digits=8, decimal_places=2, blank=False, null=False)
    product_shelf_life_seconds = models.PositiveSmallIntegerField(db_column='Product_shelf_life_seconds', blank=False, null=False)
    is_deleted = models.BooleanField(db_column='Is_deleted', default = False) #Only changeable through marking the corresponding InventoryItems record as deleted

    class Meta:
        managed = False
        db_table = 'Products'

#Accessess sales
class Sales(models.Model):
    sale_id = models.AutoField(db_column='Sale_ID', primary_key=True)
    branch_id = models.ForeignKey(Branches, models.DO_NOTHING, db_column='Branch_ID')
    sale_date_time = models.DateTimeField(db_column='Sale_date_time', blank=False, null=False)
    is_card_payment = models.BooleanField(db_column='Is_card_payment', blank=False, null=False)
    is_deleted = models.BooleanField(db_column='Is_deleted', default = False)

    class Meta:
        managed = False
        db_table = 'Sales'

#Accesses the products sold within sales
class SaleProducts(models.Model):
    pk = models.CompositePrimaryKey('sale_id', 'product_id')
    sale_id = models.ForeignKey('Sales', models.DO_NOTHING, db_column='Sale_ID')
    product_id = models.ForeignKey(Products, models.DO_NOTHING, db_column='Product_ID')
    product_quantity = models.PositiveSmallIntegerField(db_column='Product_quantity' , blank=False, null=False)
    is_deleted = models.BooleanField(db_column='Is_deleted', default = False)

    class Meta:
        managed = False
        db_table = 'Sale_products'

#Accesses stock level for each branch
class ItemStock(models.Model):
    stock_id = models.AutoField(db_column='Stock_ID', primary_key=True)
    item = models.ForeignKey(InventoryItems, models.DO_NOTHING, db_column='Item_ID')
    branch = models.ForeignKey(Branches, models.DO_NOTHING, db_column='Branch_ID')
    item_quantity = models.PositiveSmallIntegerField(db_column='Item_quantity', blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'Item_stock'
        unique_together = (('item', 'branch'),)

#Accesses the ingredients needed to make 1 of a product
class ProductIngredients(models.Model):
    pk = models.CompositePrimaryKey('product_id', 'ingredient_id')
    product_id = models.ForeignKey(Products, models.DO_NOTHING, db_column='Product_ID')
    ingredient_id = models.ForeignKey(InventoryItems, models.DO_NOTHING, db_column='Ingredient_ID')
    ingredient_quantity = models.PositiveSmallIntegerField(db_column='Ingredient_quantity', blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'ProductIngredients'