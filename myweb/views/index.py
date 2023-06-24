from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import hashlib
from myweb.models import Employee,Warehouse,Corporation,Orders, OInclude, Commodity,Inventory
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
import json
from django.http import JsonResponse
from decimal import Decimal
from collections import defaultdict
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
import decimal
# Create your views here.

def index(request):
  request.session['ordertype']=1
  cor=Corporation.objects.all()
  corlen=len(cor)
  today = timezone.now()
  start_of_today = datetime.combine(today, datetime.min.time())
  end_of_today = datetime.combine(today, datetime.max.time())
  today_orders_count = Orders.objects.filter(date__range=(start_of_today, end_of_today)).count()
  war=Warehouse.objects.all()
  warcount=0
  for i in war:
    warcount+=i.total
  ors=Orders.objects.filter(type=1)
  orlen=len(ors)
  context={"corlen":corlen,"warcount":warcount,"orlen":orlen,"today_orders_count":today_orders_count}
  return render(request,'index/index.html',context)

  # 管理员登录表单
def login(request):
    print(1)
    print(request)
    return render(request, "index/login.html")

# 提交管理员登录表单
def dologin(request):
    print(2)
    print(request)
    try:
        user = Employee.objects.get(username=request.POST['user_name'])
        print("账号:", user.user_name)
        print("状态：",user.type)
        if user.type == 0:
            md5 = hashlib.md5()
            s = request.POST['password'] + user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                print("登录成功！")
                # 将当前成功登陆的账号以字典的形式写入session
                request.session['adminuser'] = user.toDict()
                return redirect(reverse("index"))
            else:
                context = {"info":"登录密码错误！"}
        else:
            context = {"info":"无效的登录账户！"}  
    except Exception as err:
        print(err)
        context = {"info":"登录的账号不存在"}
    print(2)
    print(request)
    return render(request, "index/login.html", context)
        

# 退出管理员登录
def logout(request):
    del request.session['adminuser']
    return render(request, "index/login.html")

#销量统计
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
def statistics(request):
    # 获取当前日期
    today = timezone.now()

    # 计算7天前的日期
    date_7_days_ago = today - timedelta(days=6)

    # 获取过去7天的销售订单
    orders_7_days = Orders.objects.filter(date__range=[date_7_days_ago, today], type='1')

    # 获取这些订单中的商品及其每天的销售额
    sales_7_days = OInclude.objects.filter(order__in=orders_7_days).values('commodity__name', 'order__date').annotate(daily_sales=Sum(F('amount')))

    # 构建数据
    data_dict = defaultdict(lambda: defaultdict(int))
    total_sales = defaultdict(int)
    for sale in sales_7_days:
        date_str = sale['order__date'].date().strftime('%Y-%m-%d')
        data_dict[sale['commodity__name']][date_str] += sale['daily_sales']
        total_sales[sale['commodity__name']] += sale['daily_sales']

    # 对于没有销售的日期填充0
    date_range = [date_7_days_ago.date() + timedelta(days=i) for i in range(7)]
    date_range_str = [date.strftime('%Y-%m-%d') for date in date_range]
    for product_sales in data_dict.values():
        for date_str in date_range_str:
            product_sales.setdefault(date_str, 0)

    # 将数据格式化以适配ECharts配置
    line_data_list = [['date'] + date_range_str]
    for product, sales in data_dict.items():
        line_data_list.append([product] + [sales[date_str] for date_str in date_range_str])

    pie_data_list = [[product, total] for product, total in total_sales.items()]

    # 将数据转换为JSON
    line_data_list_json = json.dumps(line_data_list, cls=DecimalEncoder)
    pie_data_list_json = json.dumps(pie_data_list, cls=DecimalEncoder)

    # 将数据传递给模板
    data = {
        'line_data': line_data_list_json,
        'pie_data': pie_data_list_json,
    }
    return JsonResponse(data)


def todaysales(request):
    # 获取今天的日期
    today = timezone.now().date()

    # 创建今天的开始和结束时间
    start_of_today = datetime.combine(today, datetime.min.time())
    end_of_today = datetime.combine(today, datetime.max.time())

    # 获取今天的销售订单
    today_orders = Orders.objects.filter(date__range=(start_of_today, end_of_today), type='1')

    # 获取这些订单中的商品及其销售额
    today_sales = OInclude.objects.filter(order__in=today_orders).values('commodity__name').annotate(daily_sales=Sum(F('amount')))

    # 构建数据
    data_dict = {sale['commodity__name']: sale['daily_sales'] for sale in today_sales}
    total_sales = sum(data_dict.values())

    # 将数据格式化以适配ECharts配置
    bar_data_list = [[product, sales] for product, sales in data_dict.items()]

    # 将数据转换为JSON
    bar_data_list_json = json.dumps(bar_data_list, cls=DecimalEncoder)

    # 将数据传递给模板
    data = {
        'bar_data': bar_data_list_json,
        'total_sales': total_sales,
    }
    return JsonResponse(data)

from django.db.models import Sum

def warehouse_inventory(request):
    # 获取所有仓库
    warehouses = Warehouse.objects.all()

    # 获取所有商品
    commodities = Commodity.objects.all()

    # 初始化数据
    data = []
    for warehouse in warehouses:
        warehouse_data = {
            'name': warehouse.name,
            'type': 'bar',
            'stack': '总量',
            'data': []
        }
        for commodity in commodities:
            # 获取该仓库中该商品的库存数量
            quantity = Inventory.objects.filter(warehouse=warehouse, commodity=commodity).aggregate(Sum('quantity'))['quantity__sum'] or 0
            warehouse_data['data'].append(quantity)
        data.append(warehouse_data)

    # 获取所有商品的名称
    commodity_names = [commodity.name for commodity in commodities]

    return JsonResponse({
        'commodity_names': commodity_names,
        'data': data,
    })
