from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    Group.objects.create(name="baker")
    Group.objects.create(name="manager")
    Group.objects.create(name="shop assistant")
    Group.objects.create(name="till")

class Migration(migrations.Migration):
    dependencies = [('stock_management_ui', '0001_initial')]
    operations = [
        migrations.RunPython(create_groups),
    ]