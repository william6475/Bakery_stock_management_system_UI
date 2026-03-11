from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.contrib.auth.models import User, Group


def create_users(apps, schema_editor):
    #Create a password variable so that the password is not hashed multiple times into different hashes
    password = make_password("securepassword123")
    sample_baker, useless = User.objects.get_or_create(username="baker", defaults={"password": password})
    sample_manager, useless = User.objects.get_or_create(username="manager", defaults={"password": password})
    sample_shop_assistant, useless = User.objects.get_or_create(username="shop assistant", defaults={"password": password})
    sample_till, useless = User.objects.get_or_create(username="till", defaults={"password": password})


    #Add the users to their corresponding groups
    baker_group = Group.objects.get(name="baker")
    sample_baker.groups.add(baker_group)

    manager_group = Group.objects.get(name="manager")
    sample_manager.groups.add(manager_group)

    shop_assistant_group = Group.objects.get(name="shop assistant")
    sample_shop_assistant.groups.add(shop_assistant_group)

    till_group = Group.objects.get(name="till")
    sample_till.groups.add(till_group)




class Migration(migrations.Migration):
    dependencies = [('stock_management_ui', '0003_delete_deliveries_delete_deliveryitems')]
    operations = [
        migrations.RunPython(create_users),
    ]