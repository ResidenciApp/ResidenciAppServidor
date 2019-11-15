# Generated by Django 2.2.5 on 2019-10-30 01:33

from django.db import migrations, models

# https://stackoverflow.com/a/39742847/3627387

def add_roles(apps, schema_editor):

    Role = apps.get_model("Users", "Role")

    user = Role(name='Usuario', description='')
    user.save()

    admin = Role(name='Administrador', description='')
    admin.save()

    owner = Role(name='Propietario', description='')
    owner.save()


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_roles),
    ]