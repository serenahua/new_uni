# Generated by Django 4.2.4 on 2023-09-02 12:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('chicken', models.BooleanField(default=False)),
                ('hot_pot', models.BooleanField(default=False)),
                ('home', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('chicken', models.BooleanField(default=False)),
                ('hot_pot', models.BooleanField(default=False)),
                ('volume', models.PositiveSmallIntegerField(default=0)),
                ('value', models.PositiveSmallIntegerField(default=0)),
                ('remark', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('value', models.PositiveSmallIntegerField(default=0)),
                ('remark', models.TextField(blank=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.expenseitem')),
            ],
        ),
    ]
