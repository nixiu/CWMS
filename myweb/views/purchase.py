# 订单管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime, timedelta
from django.utils import timezone
import random
from myweb.models import Commodity,Inventory,Warehouse,Orders,Corporation,EmOrder,Employee,OInclude,CorSubmit
from django.views.decorators.csrf import csrf_exempt  # 导入免除csrf验证的装饰器
from django.template.loader import render_to_string
from django.core import serializers
from django.core.cache import cache
import logging


def index(request,pIndex):
    """浏览信息"""
    cache_key = "purchase_list"
    cached_data = cache.get(cache_key)
    if cached_data:
        cs=cached_data
    else:
      cs=CorSubmit.objects.filter(order__type=2)#找到对应的订单
      cache.set(cache_key, cs, 3600)
    mywhere=[]#封装条件


    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询商家名称或者日期中只要含有关键字的都可以
        cs = cs.filter(Q(cor__cor_name__contains=kw)|Q(date__contains=kw))
        mywhere.append("keyword="+kw)
    # 获取、判断并封装日期搜索
    date_filter = request.GET.get("date", None)
    print("date_filter",date_filter)
    if date_filter:
      try:
          # 转换日期字符串为datetime对象

          selected_date = datetime.strptime(date_filter, "%Y-%m-%d")
          # 创建一个时区感知的 datetime 对象
          selected_date = timezone.make_aware(selected_date, timezone=timezone.get_default_timezone())
          # 获取所选日期的下一天作为结束日期
          next_day = selected_date + timedelta(days=1)
          # 根据日期范围过滤订单
          cs = cs.filter(order__date__range=(selected_date, next_day))
          mywhere.append("date="+date_filter)
      except Exception as e:
          print("Exception when filtering by date: ", e)   
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(cs, 10)  # 以10条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    
    # p判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息
    
    # 封装信息加载模板
    context= {"orderlist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}

    return render(request, 'purchase/index.html', context)


def delete(request, uid=0):
    """执行信息删除"""
    try:
        co=Commodity.objects.get(id=uid)#得到要删除的商品
        inv = Inventory.objects.get(commodity=co)#找到对应的库存单
        wa=inv.warehouse#对应的仓库
        wa.total=wa.total-inv.amount#删除商品前要把库存删掉
        co.delete()
        cache_key = "purchase_list"
        cache.delete(cache_key)
        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    # return JsonResponse(context)
    return render(request, "info.html", context)

def order_detail(request, orderId):
    order = Orders.objects.get(id=orderId)
    order_details = OInclude.objects.filter(order=orderId)
    for detail in order_details:
        print(detail.id, detail.commodity.name, detail.quantity)  # 输出每个OInclude对象的字段
    cor_submit = CorSubmit.objects.get(order=order)  # 获取相关的公司提交信息
    corporation = cor_submit.cor  # 获取相关的公司信息
    rendered_html = render_to_string('sale/order_detail.html', {'order': order, 'order_details': order_details, 'corporation': corporation}, request=request)
    return JsonResponse({'rendered_html': rendered_html})