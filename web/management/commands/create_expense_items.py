from django.core.management import BaseCommand

from web.models import ExpenseItem


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 建立支出項目
        # 馥香雞 8 items
        ExpenseItem.objects.create(name="租金", chicken=True)
        ExpenseItem.objects.create(name="稅金", chicken=True)
        ExpenseItem.objects.create(name="加油", chicken=True)
        ExpenseItem.objects.create(name="停車月費", chicken=True)
        ExpenseItem.objects.create(name="市場管理費", chicken=True)
        ExpenseItem.objects.create(name="貨款", chicken=True)
        ExpenseItem.objects.create(name="員工薪資", chicken=True)
        ExpenseItem.objects.create(name="消耗品", chicken=True)

        # 日料、小菜 4 items
        ExpenseItem.objects.create(name="火鍋料貨款", hot_pot=True)
        ExpenseItem.objects.create(name="肉片貨款", hot_pot=True)
        ExpenseItem.objects.create(name="小菜貨款", hot_pot=True)
        ExpenseItem.objects.create(name="消耗品", hot_pot=True)

        # 家庭開銷 25 items
        ExpenseItem.objects.create(name="孝親費", home=True)
        ExpenseItem.objects.create(name="川匯豐卡", home=True)
        ExpenseItem.objects.create(name="川第一卡", home=True)
        ExpenseItem.objects.create(name="川玉山卡", home=True)
        ExpenseItem.objects.create(name="金富邦momo卡", home=True)
        ExpenseItem.objects.create(name="金富邦財神卡", home=True)
        ExpenseItem.objects.create(name="金台新玫瑰giving卡", home=True)
        ExpenseItem.objects.create(name="川phone", home=True)
        ExpenseItem.objects.create(name="金phone", home=True)
        ExpenseItem.objects.create(name="住管費", home=True)
        ExpenseItem.objects.create(name="住水費", home=True)
        ExpenseItem.objects.create(name="住電費", home=True)
        ExpenseItem.objects.create(name="住天然氣", home=True)
        ExpenseItem.objects.create(name="按摩", home=True)
        ExpenseItem.objects.create(name="師父祈福", home=True)
        ExpenseItem.objects.create(name="川年保費", home=True)
        ExpenseItem.objects.create(name="金年保費", home=True)
        ExpenseItem.objects.create(name="小冬瓜年保費", home=True)
        ExpenseItem.objects.create(name="川&金季勞保費", home=True)
        ExpenseItem.objects.create(name="重機", home=True)
        ExpenseItem.objects.create(name="Jaguar", home=True)
        ExpenseItem.objects.create(name="黃牌", home=True)
        ExpenseItem.objects.create(name="紅牌", home=True)
        ExpenseItem.objects.create(name="川購物", home=True)
        ExpenseItem.objects.create(name="金購物", home=True)
        pass
