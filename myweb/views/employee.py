# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
import random
from myweb.models import Employee
from django.core.cache import cache

def index(request, pIndex):
    """浏览信息"""
    cache_key = "employee_list"
    cached_data = cache.get(cache_key)

    if cached_data:
        # 如果缓存中存在数据，则直接使用缓存数据
        ulist = cached_data
    else:
        umod = Employee.objects
        ulist = umod.filter(type__lt=3)  # 3类型的员工账号已经无效不应该显示

        

        # 将数据缓存到Redis中，有效期设置为1小时
        cache.set(cache_key, ulist, timeout=3600)
    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询员工账号或昵称中只要含有关键字的都可以
        ulist = ulist.filter(Q(name__contains=kw) | Q(user_name__contains=kw))

    # 获取、判断并封装状态type搜索条件
    type = request.GET.get('type', '')
    if type != '':
        ulist = ulist.filter(type=type)
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 以10条每页创建分页对象
    maxpages = page.num_pages  # 最大页数

    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    # 封装信息加载模板
    context = {"Employeelist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages}

    return render(request, 'employee/index.html', context)

def add(request):
    """加载信息添加表单"""
    return render(request, "employee/add.html")

def insert(request):
    """执行信息添加"""
    try:
        ob = Employee()
        ob.user_name = request.POST["user_name"]#账户名称
        ob.name = request.POST["name"]#员工姓名
        #ob.password = request.POST['password']#密码将来可以做加密操作
        # 获取密码并MD5
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n)#获取密码并添加干扰值
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.phone=request.POST["phone"]
        ob.type = request.POST["type"]
        ob.save()
        cache_key = "employee_list"
        cache.delete(cache_key)
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败！"}
    return render(request, "info.html", context)

def delete(request, uid=0):
    """执行信息删除"""
    try:
        ob = Employee.objects.get(id=uid)
        ob.type = 3#失效
        ob.save()
        cache_key = "employee_list"
        cache.delete(cache_key)
        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    # return JsonResponse(context)
    return render(request, "info.html", context)

def edit(request, uid=0):
    """加载信息编辑表单"""
    try:
        ob = Employee.objects.get(id=uid)
        context={"Employee":ob}
        return render(request, 'employee/edit.html',context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"info.html",context)
    

def update(request, uid):
    """执行信息编辑"""
    try:
        ob = Employee.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.type = request.POST['type']
        ob.phone=request.POST['phone']
        ob.user_name=request.POST['user_name']
        ob.save()
        cache_key = "employee_list"
        cache.delete(cache_key)
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"info.html",context)