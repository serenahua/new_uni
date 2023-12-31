# Generated by Django 4.2.4 on 2023-09-02 12:47

from django.db import migrations


def create_settings(apps, schema_editor):
    fake_model = apps.get_model('web', 'Setting')
    fake_model.objects.create(name="name", value="記帳小程式")
    fake_model.objects.create(name="color", value="1")


def delete_settings(apps, schema_editor):
    fake_model = apps.get_model('web', 'Setting')
    fake_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_settings, delete_settings)
    ]
