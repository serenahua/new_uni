# Generated by Django 4.2.4 on 2023-10-03 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_seed'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='house',
            field=models.BooleanField(default=False),
        ),
    ]
