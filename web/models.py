from django.db import models
from django.utils import timezone

from auditlog.registry import auditlog

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

    @property
    def category(self) -> str:
        cate = 'chicken' if self.item.chicken else 'hot_pot' if self.item.hot_pot else 'home'
        return cate


class Income(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    chicken = models.BooleanField(default=False)
    hot_pot = models.BooleanField(default=False)
    house = models.BooleanField(default=False)
    volume = models.PositiveSmallIntegerField(default=0)
    value = models.PositiveSmallIntegerField(default=0)
    remark = models.TextField(blank=True)

    @property
    def classname(self) -> str:
        return 'income'

    @property
    def category(self) -> str:
        cate = 'chicken' if self.chicken else 'hot_pot' if self.hot_pot else 'home'
        return cate


class Setting(models.Model):
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)


# https://django-auditlog.readthedocs.io/en/latest/usage.html
auditlog.register(ExpenseItem)
auditlog.register(Expense)
auditlog.register(Income)
auditlog.register(Setting)