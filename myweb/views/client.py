# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
import random
from myweb.models import Commodity,Corporation


def index(request,pIndex):
    """浏览信息"""
    umod =  Corporation.objects
    mywhere=[]#封装条件
    ulist = umod.filter(cor_type=1)#1类型为客户  2为供货商  

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询客户姓名或电话中只要含有关键字的都可以
        ulist = ulist.filter( Q(cor_name__contains=kw) | Q(cor_phone__contains=kw))
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
    context= {"Corporationlist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}

    return render(request, 'client/index.html', context)

def add(request):
    """加载信息添加表单"""
    return render(request, "client/add.html")

def insert(request):
    """执行信息添加"""
    try:
        ob = Corporation()
        ob.cor_name = request.POST["name"]#公司名称
        ob.cor_type = 1#固定为客户
        ob.cor_address=request.POST["address"]
        ob.cor_phone=request.POST["phone"]
        ob.cor_contact=request.POST["contact"]
        ob.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败！"}
    return render(request, "info.html", context)

def delete(request, uid=0):
    """执行信息删除"""
    try:
        Corporation.objects.get(id=uid).delete()
        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    # return JsonResponse(context)
    return render(request, "info.html", context)

def edit(request, uid=0):
    """加载信息编辑表单"""
    try:
        ob = Corporation.objects.get(id=uid)
        context={"Corporation":ob}
        return render(request, 'client/edit.html',context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"info.html",context)
    

def update(request, uid):
    """执行信息编辑"""
    try:
        ob = Corporation.objects.get(id=uid)
        ob.cor_name = request.POST["name"]#公司名称
        ob.cor_type = 1#固定为客户
        ob.cor_address=request.POST["address"]
        ob.cor_phone=request.POST["phone"]
        ob.cor_contact=request.POST["contact"]
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"info.html",context)