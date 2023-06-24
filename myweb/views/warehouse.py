# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
import random
from myweb.models import Commodity,Inventory,Warehouse


def index(request,pIndex):
    """浏览信息"""
    umod = Warehouse.objects
    mywhere=[]#封装条件
    ulist = umod.all()

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询仓库名称或仓库总管中只要含有关键字的都可以
        ulist = ulist.filter(Q(name__contains=kw)|Q(explorer__contains=kw))
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
    print("aaaaaaaaaaaaaaaaaa")
    print(list2[0].total)
    # 封装信息加载模板
    context= {"Warehouselist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}

    return render(request, 'warehouse/index.html', context)

def add(request):
    """加载信息添加表单"""
    return render(request, "warehouse/add.html")

def insert(request):
    """执行信息添加"""
    try:
        wa=Warehouse()
        wa.name=request.POST["name"]#仓库名
        wa.explorer=request.POST["explorer"]#仓库主管
        wa.phone=request.POST["phone"]#联系方式
        wa.address=request.POST["address"]#仓库地址
        wa.total=0#总金额初始为0
        wa.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败！"}
    return render(request, "info.html", context)

def delete(request, uid=0):
    """执行信息删除"""
    try:
        Warehouse.objects.get(id=uid).delete()
        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    # return JsonResponse(context)
    return render(request, "info.html", context)

def edit(request, uid=0):
    """加载信息编辑表单"""
    try:
        wa=Warehouse.objects.get(id=uid)
        context={"Warehouse":wa}
        return render(request, 'warehouse/edit.html',context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        print(err)
        return render(request,"info.html",context)
    

def update(request, uid):
    """执行信息编辑"""
    try:
        wa=Warehouse.objects.get(id=uid)
        wa.name=request.POST["name"]#仓库名
        wa.explorer=request.POST["explorer"]#仓库主管
        wa.phone=request.POST["phone"]#联系方式
        wa.address=request.POST["address"]#仓库地址
        wa.save()#仓库库存在商品以及订单修改时改变
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"info.html",context)