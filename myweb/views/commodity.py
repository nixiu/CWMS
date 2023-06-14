# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
import random
from myweb.models import Commodity,Inventory,Warehouse
import decimal

def index(request,pIndex):
    """浏览信息"""
    umod = Inventory.objects.order_by("commodity__id")
    mywhere=[]#封装条件
    ulist = umod.all()#3类型的员工账号已经无效不应该显示

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询商品名称中只要含有关键字的都可以
        ulist = ulist.filter(Q(commodity__name__contains=kw))
        mywhere.append("keyword="+kw)
        
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 以10条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    
    # p判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息
    
    # 封装信息加载模板
    context= {"Commoditylist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}

    return render(request, 'commodity/index.html', context)

def add(request):
    """加载信息添加表单"""
    wlist=Warehouse.objects.all()
    contex={"warehouselist":wlist}
    return render(request, "commodity/add.html",contex)

def insert(request):
    """执行信息添加"""
    try:
        co=Commodity()#初始化一个商品
        ob = Inventory()#初始化一个商品对应库存表
        co.name=request.POST["name"]#商品名称
        co.unitprice=request.POST["unitprice"]#单价
        co.costprice=request.POST["costprice"]#成本价
        ob.quantity=request.POST["quantity"]#数量
        ob.amount=decimal.Decimal(co.unitprice)*decimal.Decimal(ob.quantity)#库存金额计算
        ob.commodity=co#库存表对应商品
        warehouseid=request.POST["warehouse"]#找到存放的存放仓库
        war=Warehouse.objects.get(id=warehouseid)
        war.total=war.total+ob.amount#修改该仓库的库存总金额
        war.save(update_fields=['total'])#只需更新总金额
        ob.warehouse=war#库存表对应的仓库
        co.save()#储存数据
        ob.save()#储存数据
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败！"}
    return render(request, "info.html", context)

def delete(request, uid=0):
    """执行信息删除"""
    try:
        co=Commodity.objects.get(id=uid)#得到要删除的商品
        inv = Inventory.objects.get(commodity=co)#找到对应的库存单
        wa=inv.warehouse#对应的仓库
        wa.total=wa.total-inv.amount#删除商品前要把库存删掉
        wa.save()
        co.delete()

        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    # return JsonResponse(context)
    return render(request, "info.html", context)

def edit(request, uid=0):
    """加载信息编辑表单"""
    try:
        ob = Commodity.objects.get(id=uid)#找到修改的商品
        inv = Inventory.objects.get(commodity=ob)#找到对应的库存单
        war=inv.warehouse#找到相应的仓库
        war.total=war.total-inv.amount#编辑前把库存改一下防止更改仓库
        war.save(update_fields=['total'])#只需更新总金额
        wlist=Warehouse.objects.all()#全部仓库
        context={"Commodity":ob,"Inventory":inv,"Warehouse":war,"warehouselist":wlist}
        return render(request, 'commodity/edit.html',context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        print(err)
        return render(request,"info.html",context)
    

def update(request, uid):
    """执行信息编辑"""
    try:
        co = Commodity.objects.get(id=uid)#找到修改的商品
        ob = Inventory.objects.get(commodity=co)#找到对应的库存单
        co.name=request.POST["name"]#商品名称
        co.unitprice=request.POST["unitprice"]#单价
        co.costprice=request.POST["costprice"]#成本价
        ob.quantity=request.POST["quantity"]
        ob.amount=decimal.Decimal(co.unitprice)*decimal.Decimal(ob.quantity)#库存金额计算
        ob.commodity=co
        warehouseid=request.POST["warehouse"]#存放仓库
        warehouse=Warehouse.objects.get(id=warehouseid)
        warehouse.total=warehouse.total+ob.amount#更新库存
        warehouse.save(update_fields=['total'])#只需更新总金额
        ob.warehouse=warehouse
        co.save()
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"info.html",context)