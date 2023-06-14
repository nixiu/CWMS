# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
import random
from myweb.models import Commodity,Inventory,Warehouse,Orders,Corporation,EmOrder,Employee,OInclude,CorSubmit


def index(request,pIndex):
    """浏览信息"""
    cs=CorSubmit.objects.filter(order__type=1)#找到对应的客户关系表

    # saleorder=Orders.objects.filter(type=1)
    # saleorder=saleorder.order_by(id)#得到销售单并排序
    # cor=cs.cor#对应的商家
    # eo=EmOrder.objects.get(or_field=saleorder)#处理职员关系表

    mywhere=[]#封装条件


    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询商家名称或者日期中只要含有关键字的都可以
        cs = cs.filter(Q(cor__cor_name__contains=kw)|Q(date__contains=kw))
        mywhere.append("keyword="+kw)
        
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

    return render(request, 'sale/index.html', context)


def delete(request, uid=0):
    """执行信息删除"""
    try:
        co=Commodity.objects.get(id=uid)#得到要删除的商品
        inv = Inventory.objects.get(commodity=co)#找到对应的库存单
        wa=inv.warehouse#对应的仓库
        wa.total=wa.total-inv.amount#删除商品前要把库存删掉
        co.delete()

        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    # return JsonResponse(context)
    return render(request, "info.html", context)

def detail(request):
  pass