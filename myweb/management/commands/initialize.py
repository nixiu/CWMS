from django.core.management.base import BaseCommand
from myweb.models import Commodity, Inventory, Warehouse
import decimal

class Command(BaseCommand):
    help = 'Initialize warehouse totals'

    def handle(self, *args, **options):
        try:
            # 遍历所有的库存项
            for inv in Inventory.objects.all():
                # 重新计算库存金额
                inv.amount = decimal.Decimal(inv.commodity.unitprice) * decimal.Decimal(inv.quantity)
                inv.save(update_fields=['amount'])

            # 遍历所有的仓库
            for war in Warehouse.objects.all():
                # 重新计算仓库总金额
                war.total = sum(inv.amount for inv in Inventory.objects.filter(warehouse=war))
                war.save(update_fields=['total'])

            self.stdout.write(self.style.SUCCESS('Successfully initialized warehouse totals'))
        except Exception as err:
            self.stdout.write(self.style.ERROR('Failed to initialize warehouse totals'))
            self.stdout.write(self.style.ERROR(str(err)))