from django.test import TestCase
from stock_management_ui.models import Branches, Deliveries, InventoryItems, DeliveryItems, Products, Sales, SaleProducts, ItemStock, ProductIngredients

# Create your tests here.
#NOTE: THIS IS IN THE CORRECT TEST FORMAT MABY JUST DELETE AND MAKE TESTS FROM SCRATCH
branch = Branches.objects.get(branch_id = 2)
print(branch.branch_id, branch.branch_name, branch.branch_phone_number, branch.branch_city, branch.is_deleted)

