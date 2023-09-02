from django.db import models
from django.utils import timezone


class ExpenseItem(models.Model):
    name = models.CharField(max_length=128)
    chicken = models.BooleanField(default=False)
    hot_pot = models.BooleanField(default=False)
    home = models.BooleanField(default=False)


class Expense(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(ExpenseItem, on_delete=models.SET_NULL, null=True)
    value = models.PositiveSmallIntegerField(default=0)
    remark = models.TextField(blank=True)

    @property
    def classname(self) -> str:
        return 'expense'


class Income(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    chicken = models.BooleanField(default=False)
    hot_pot = models.BooleanField(default=False)
    volume = models.PositiveSmallIntegerField(default=0)
    value = models.PositiveSmallIntegerField(default=0)
    remark = models.TextField(blank=True)

    @property
    def classname(self) -> str:
        return 'income'


class Setting(models.Model):
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)