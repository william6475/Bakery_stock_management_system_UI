from django.forms import ModelForm
from .models import Branches, InventoryItems, Products, Sales, SaleProducts, ItemStock, ProductIngredients


class BranchesForm(ModelForm):
    class Meta:
        model=Branches
        fields = ["branch_name", "branch_phone_number", "branch_city", "is_deleted"]

class InventoryItemsForm(ModelForm):
    class Meta:
        model=InventoryItems
        fields = ["item_name", "item_cost", "item_category", "is_deleted"]

class ProductsForm(ModelForm):
    class Meta:
        model=Products
        fields = ["item_id", "product_category", "product_price", "product_shelf_life_seconds", "is_deleted"]

class SalesForm(ModelForm):
    class Meta:
        model=Sales
        fields = ["branch_id", "sale_date_time", "is_card_payment", "is_deleted"]

class SaleProductsForm(ModelForm):
    class Meta:
        model=SaleProducts
        fields=["sale_id", "product_id", "product_quantity", "is_deleted"]

class ItemStockForm(ModelForm):
    class Meta:
        model=ItemStock
        fields = ["item_id", "branch", "item_quantity"]

class ProductIngredientsForm(ModelForm):
    class Meta:
        model=ProductIngredients
        fields = ["product_id", "ingredient_id", "ingredient_quantity"]