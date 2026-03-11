from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase

# Create your tests here.
def can_access_sales(request):
    if request.groups.filter(name='till').exists():
        return True
    elif request.groups.filter(name='manager').exists():
        return True
    elif request.groups.filter(name='shop assistant').exists():
        return True
    else:
        return False

