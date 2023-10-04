from datetime import datetime, timedelta, time
from itertools import chain
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import get_messages
from django.db.models import Q, Sum, Case, When, DateTimeField, CharField, BooleanField
from django.db.models.functions import TruncDate, Cast
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView

from .models import ExpenseItem, Expense, Income, Setting


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "home"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        now = timezone.now()

        # 用一個字典来儲存不同類別的收入和支出
        categories = {
            'chicken': {'income_filter': {'chicken': True}, 'expense_filter': {'item__chicken': True}},
            'hotpot': {'income_filter': {'hot_pot': True}, 'expense_filter': {'item__hot_pot': True}},
            'home': {'income_filter': {'house': True}, 'expense_filter': {'item__home': True}}
        }

        totals = {}
        volume = 0

        # 計算不同類別的收入和支出
        for category, filters in categories.items():
            income_filter = filters.get('income_filter', {})  # 获取 'income_filter' 键的值，如果不存在则返回空字典
            expense_filter = filters.get('expense_filter', {})  # 获取 'expense_filter' 键的值，如果不存在则返回空字典

            incomes = Income.objects.filter(date__year=now.year, date__month=now.month, **income_filter)
            expenses = Expense.objects.filter(date__year=now.year, date__month=now.month, **expense_filter)

            total_income = sum([income.value for income in incomes])
            total_expense = sum([expense.value for expense in expenses])
            total = total_income - total_expense

            totals[category] = total

            if category == 'chicken':
                volume = sum([income.volume for income in incomes])

        # 計算總和
        total = sum(totals.values())

        context.update(totals)
        context['volume'] = volume
        context['total'] = total

        return context


class TrackingView(LoginRequiredMixin, TemplateView):
    template_name = 'web/tracking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "tracking"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        calendar_head = ['日','一','二','三','四','五','六']
        context['calendar_head'] = calendar_head

        today = datetime.now()
        context['today'] = today

        return context


class TrackingFormView(LoginRequiredMixin, TemplateView):
    template_name = 'web/tracking_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "tracking"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        date = request.GET.get('date')
        item_id = request.GET.get('n')
        category = request.GET.get('c')

        tab = request.GET.get('t', 0)
        context['tab'] = tab

        if not date and not item_id:
            return HttpResponseRedirect(reverse_lazy('web:tracking'))

        if category == 'i':
            item = Income.objects.get(id=item_id)
            context['item'] = item
            context['date'] = item.date
        elif category == 'e':
            item = Expense.objects.get(id=item_id)
            context['item'] = item
            context['date'] = item.date
        else:
            context['date'] = date

        context['expense_items'] = {
            'chicken': list(ExpenseItem.objects.filter(chicken=True).values('id', 'name')),
            'hotpot': list(ExpenseItem.objects.filter(hot_pot=True).values('id', 'name')),
            'house': list(ExpenseItem.objects.filter(home=True).values('id', 'name')),
        }

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        method = request.POST['method']
        date = request.POST['date']
        item_id = request.POST.get('id')
        type = request.POST['type']
        item_name = request.POST['item_name']
        category = request.POST.get('category')
        value = request.POST['value']
        chicken = request.POST.get('chicken')
        remark = request.POST['remark']


        if method == 'edit':
            if type == 'income':
                item = Income.objects.get(id=item_id)
            elif type == 'expense':
                item = Expense.objects.get(id=item_id)
        elif method == 'create':
            item = Income() if type == 'income' else Expense()

        item.date = date
        item.value = value
        item.remark = remark

        if type == 'income':
            if chicken:
                item.volume = chicken
            if item_name in ('chicken', 'hot_pot', 'house'):
                setattr(item, item_name, True)
        elif type == 'expense':
            item.item_id = category

        item.save()

        return JsonResponse({'status': True})


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'web/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "report"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        calendar_head = ['日','一','二','三','四','五','六']
        context['calendar_head'] = calendar_head

        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        now = timezone.now()

        type = request.GET.get('t', 'm')
        date_str = request.GET.get('date')
        tab = request.GET.get('tab', '0')
        date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else now
        year = date.year
        month = date.month

        if type == 'm':
            incomes = Income.objects.filter(date__year=year, date__month=month)
            expenses = Expense.objects.filter(date__year=year, date__month=month, item__isnull=False)

            if tab == '1':
                incomes = incomes.filter(chicken=True)
                expenses = expenses.filter(item__chicken=True)
            elif tab == '2':
                incomes = incomes.filter(hot_pot=True)
                expenses = expenses.filter(item__hot_pot=True)
            elif tab == '3':
                incomes = incomes.filter(house=True)
                expenses = expenses.filter(item__home=True)

            # monthly data
            monthly_volume = incomes.aggregate(Sum('volume'))['volume__sum'] or 0
            monthly_income = incomes.aggregate(Sum('value'))['value__sum'] or 0
            monthly_expense = expenses.aggregate(Sum('value'))['value__sum'] or 0
            monthly_total = monthly_income - monthly_expense

            context['total'] = monthly_total
            context['income'] = monthly_income
            context['expense'] = monthly_expense
            context['volume'] = monthly_volume

            # daily data
            has_remark = Case(
                When(remark='', then=False),
                default=True,
                output_field=BooleanField(),
            )

            daily_incomes = incomes.annotate(str_d=Cast(TruncDate('date', DateTimeField()), CharField())).\
                            values('str_d').\
                            annotate(income=Sum('value'), chicken=Sum('volume'), has_remark=has_remark)
            daily_expenses = expenses.annotate(str_d=Cast(TruncDate('date', DateTimeField()), CharField())).\
                            values('str_d').\
                            annotate(expense=Sum('value'), has_remark=has_remark)
            lists = sorted(list(chain(daily_incomes, daily_expenses)), key=lambda item: item['str_d'])

            # for i in range(len(lists)):
            #     if i >= len(daily_list)-1:
            #         continue
            #     elif daily_list[i]['str_d'] == daily_list[i+1]['str_d']:
            #         import pdb; pdb.set_trace()
            #         daily_list[i].update(daily_list[i+1])
            #         daily_list.pop(i+1)

            # for item in daily_list:
            #     inc = item.get('income', 0)
            #     exp = item.get('expense', 0)
            #     item['total'] = inc - exp

            # import pdb; pdb.set_trace()
            context['daily_items'] = json.dumps(lists)
        elif type == 'd':
            incomes = Income.objects.filter(date__contains=date)
            expenses = Expense.objects.filter(date__contains=date,item__isnull=False)

            if tab == '1':
                incomes = incomes.filter(chicken=True)
                expenses = expenses.filter(item__chicken=True)
            elif tab == '2':
                incomes = incomes.filter(hot_pot=True)
                expenses = expenses.filter(item__hot_pot=True)
            elif tab == '3':
                incomes = incomes.filter(house=True)
                expenses = expenses.filter(item__home=True)

            items = sorted(list(chain(incomes, expenses)), key=lambda i: i.creation, reverse=True)
            context['items'] = items

            daily_volume = incomes.aggregate(Sum('volume'))['volume__sum'] or 0
            daily_income = incomes.aggregate(Sum('value'))['value__sum'] or 0
            daily_expense = expenses.aggregate(Sum('value'))['value__sum'] or 0
            daily_total = daily_income - daily_expense

            context['total'] = daily_total
            context['income'] = daily_income
            context['expense'] = daily_expense
            context['volume'] = daily_volume

        context['date'] = date
        context['type'] = type
        context['tab'] = tab

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        method = request.POST['method']
        type = 0

        if method == 'delete_item':
            item_id = request.POST['id']
            type = request.POST['type']
            model_to_delete = Income if type == 'income' else Expense

            try:
                item_to_delete = model_to_delete.objects.get(id=item_id)
                item_to_delete.delete()
            except model_to_delete.DoesNotExist:
                pass

        return JsonResponse({
            'status': True,
            'type': type
        })

    def get_valid_date(self, year, month, day, action):
        if action == 0:
            pass
        elif action == -1 or action == 1:
            date = datetime(year, month, day)
            date += timedelta(days=action)
            year, month, day = date.year, date.month, date.day
        elif action == -30 or action == 30:
            if month == 1 and action < 0:
                year -= 1
                month = 12
            elif month == 12 and action > 0:
                year += 1
                month = 1
            else:
                month += 1 if action > 0 else -1

        return (year, month, day)


class SystemManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'web/system.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "setting"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        cat = self.request.GET.get('cat', '1')

        filters = {
            '1': {'chicken': True},
            '2': {'hot_pot': True},
            '3': {'home': True},
            '4': {}  # Empty filter for 'Setting' category
        }

        if cat != '4':
            items = ExpenseItem.objects.filter(**filters.get(cat, {})).order_by('name')
        else:
            items = Setting.objects.all()

        context['items'] = items
        context['cat'] = cat

        return context


class SystemDataView(LoginRequiredMixin, TemplateView):
    template_name = 'web/data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "setting"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        cat = self.request.GET.get('cat', '1')
        item_id = self.request.GET.get('n')

        item = None
        if item_id is not None:
            model_class = Setting if cat == '4' else ExpenseItem
            item = model_class.objects.get(id=item_id)

        context['item'] = item
        context['cat'] = cat

        return context

    def _delete_item(self, request):
        item_id = request.POST['id']
        ExpenseItem.objects.get(id=item_id).delete()

    def _create_item(self, request):
        type = request.POST['type']
        name = request.POST['name']

        item = ExpenseItem()
        item.name = name
        item.chicken = (type == 'chicken')
        item.hot_pot = (type == 'hotpot')
        item.home = (type == 'home')
        item.save()

        type = 1 if type == 'chicken' else 2 if type == 'hotpot' else 3
        return type

    def _edit_item(self, request):
        name = request.POST['name']
        item_id = request.POST['id']

        item = ExpenseItem.objects.get(id=item_id)
        item.name = name
        item.save()

        type = 1 if item.chicken else 2 if item.hot_pot else 3
        return type

    def _edit_setting(self, request):
        item_id = request.POST['id']
        value = request.POST['name']

        item = Setting.objects.get(id=item_id)
        item.value = value
        item.save()

        return 4

    def _edit_color(self, request):
        item_id = request.POST['id']
        value = str(request.POST['_color'])

        item = Setting.objects.get(id=item_id)
        item.value = value
        item.save()

        return 4

    def post(self, request, **kwargs):
        method = request.POST['method']
        type = 0

        method_functions = {
            'delete_item': self._delete_item,
            'create_item': self._create_item,
            'edit_item': self._edit_item,
            'edit_setting': self._edit_setting,
            'edit_color': self._edit_color,
        }

        if method in method_functions:
            type = method_functions[method](request)

        return JsonResponse({
            'status': True,
            'type': type
        })


class LoginView(TemplateView):
    template_name = 'web/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = Setting.objects.get(name='name')
        context['name'] = name

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        return context

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('web:index'))

        context = self.get_context_data(**kwargs)
        context['next'] = request.GET.get('next', '/')

        return self.render_to_response(context)

    def post(self, request, **kwargs):

        username = request.POST['account']
        password = request.POST['password']
        _next = request.POST['next']

        if not username or not password:
            return JsonResponse({
                'status': False,
                'error': -1,
                'msg': 'account/password not provided'
            })

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': True,
                'next': _next,
            })
        else:
            return JsonResponse({
                'status': False,
                'error': -2,
                'msg': 'account/password not provided'
            })


# 暫時用不到的頁面
class ChickenView(LoginRequiredMixin, TemplateView):
    template_name = 'web/chicken.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "chicken"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        item_id = self.request.GET.get('n')
        type = self.request.GET.get('t')

        if item_id is not None:
            item = Income.objects.get(id=item_id) if type == 'income' else Expense.objects.get(id=item_id)
            context['type'] = type
            context['item'] = item

        context['categories'] = ExpenseItem.objects.filter(chicken=True).order_by('name')
        context['today'] = timezone.now()

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        item_id = request.POST.get('id')
        type = request.POST['type']
        date = request.POST['date']
        value = request.POST['value']
        chicken = request.POST['chicken']
        category = request.POST['category']
        remark = request.POST['remark']

        if method == 'edit':
            item = Income.objects.get(id=item_id) if type == 'income' else Expense.objects.get(id=item_id)
        else:
            item = Income() if type == 'income' else Expense()

        item.date = date
        item.value = value
        item.remark = remark

        if type == 'income':
            item.volume = chicken
            item.chicken = True
        elif type == 'expense':
            item.item_id = category

        item.save()

        return JsonResponse({'status': True})


class HotPotView(LoginRequiredMixin, TemplateView):
    template_name = 'web/hotpot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "hotpot"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        item_id = self.request.GET.get('n')
        type = self.request.GET.get('t')

        if item_id is not None:
            item = Income.objects.get(id=item_id) if type == 'income' else Expense.objects.get(id=item_id)
            context['type'] = type
            context['item'] = item

        context['categories'] = ExpenseItem.objects.filter(hot_pot=True).order_by('name')
        context['today'] = timezone.now()

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        item_id = request.POST.get('id') if method == 'edit' else None
        type = request.POST.get('type')
        date = request.POST['date']
        value = request.POST['value']
        category = request.POST.get('category')
        remark = request.POST['remark']

        if item_id:
            item = Income.objects.get(id=item_id) if type == 'income' else Expense.objects.get(id=item_id)
        else:
            item = Income() if type == 'income' else Expense()

        item.date = date
        item.value = value
        item.remark = remark

        if type == 'expense':
            item.item_id = category
        else:
            item.hot_pot = True

        item.save()

        return JsonResponse({'status': True})


class HomeExpenseView(LoginRequiredMixin, TemplateView):
    template_name = 'web/expense.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "home_expense"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        item_id = self.request.GET.get('n')

        if item_id is not None:
            item = Expense.objects.get(id=item_id)
            context['item'] = item

        context['categories'] = ExpenseItem.objects.filter(home=True).order_by('name')
        context['today'] = timezone.now()

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        item_id = request.POST.get('id') if method == 'edit' else None
        date = request.POST['date']
        value = request.POST['value']
        category = request.POST['category']
        remark = request.POST['remark']

        item = Expense.objects.get(id=item_id) if item_id else Expense()
        item.date = date
        item.value = value
        item.item_id = category
        item.remark = remark
        item.save()

        return JsonResponse({'status': True})

