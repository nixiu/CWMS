# 员工信息管理的视图文件
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
from django.urls import reverse
from myweb.models import Commodity,Inventory,Warehouse,Corporation,Orders,Employee,CorSubmit,EmOrder,OInclude
from django.utils import timezone
import decimal
def index(request,pIndex):
    """浏览信息"""
    umod = Inventory.objects.order_by("commodity__id")
    mywhere=[]#封装条件
    ulist = umod.all()
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
    ew=request.session['ordertype']
    if request.session['ordertype'] is None:
      request.session['ordertype']="1"
    #获取所有商品
    clist=Commodity.objects.all()
    commoditylist=dict()
    for c in clist:
      commoditylist[c.id]=c.toDict()
    request.session['commoditylist'] = commoditylist#放到session种
    # p判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息

    #订单金额添加模块
    addorderlist = request.session.get('addorderlist', {})#订单的商品列表信息获取
    total_money = 0
    # request.session["total_money"] = total_money
    for vo in addorderlist.values():#当订单商品数量修改时执行下面操作，更新总的金额
      if request.session['ordertype'] == "1":#当订单类型为销售单时
        total_money += vo["quantity"] * float(vo["unitprice"])#总金额应该按单价乘以数量来增加
      else:
        total_money += vo["quantity"] * float(vo["costprice"])#为进货单时应该乘以成本价来更改订单总金额
    request.session["total_money"] = total_money

    #客户信息模块
    # 封装信息加载模板
    context= {"Commoditylist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}

    return render(request, 'orders/addorder.html', context)

def add(request, pid):
    """向订单中添加商品"""
    # 从session中获取所有的商品信息，并从中提取需要放入订单的商品信息
    commodity = request.session['commoditylist'][pid]
    addorderlist = request.session.get('addorderlist', {})
    
    if pid not in addorderlist:
        addorderlist[pid] = commodity
        addorderlist[pid]["quantity"]=0#初始数量为0
   
    # 将addorderlist存入session
    request.session['addorderlist'] = addorderlist
    print(addorderlist)
    
    # 跳转到点餐首页
    return redirect(reverse('addorder_index', args=[1]))
    

def delete(request, pid):
    """在订单中删除商品"""
    addorderlist = request.session.get('addorderlist', {})

    del addorderlist[pid]
    # 将addorderlist存入session
    request.session['addorderlist'] = addorderlist
    # 跳转到点餐首页
    return  redirect(reverse('addorder_index', args=[1]))
    

def clear(request):
    """清空订单"""
    request.session['addorderlist'] = {}
    # 跳转到点餐首页
    return  redirect(reverse('addorder_index', args=[1]))

def change(request):
    """更改订单信息"""
    addorderlist = request.session.get('addorderlist', {})
    pid = request.GET.get("pid", 0)  # 得到商品序号
    m = float(request.GET.get("quantity", 1))
    addorderlist[pid]["quantity"] = m
    request.session['addorderlist'] = addorderlist
    return  redirect(reverse('addorder_index', args=[1]))

    # 执行添加订单操作
def insert(request):
    try:
        # 执行订单信息添加
        od = Orders()#实例化一个订单
        od.type=request.session['ordertype']#订单类型
        od.date= timezone.now()#订单的时间
        od.total=request.session["total_money"]#订单总金额
        cs=CorSubmit()#实例化订单和往来单位的关系
        cs.order=od#对应订单
        corp=Corporation.objects.get(id=request.GET.get("corpid"))#生成订单时选择的单位
        cs.cor=corp#对应单位
        cs.date=od.date#时间
        #建立订单和职员的关系
        em=Employee.objects.get(name="杨文涛")
        eo=EmOrder()#职员关系表
        eo.em=em#对应职员
        eo.or_field =od#对应订单
        eo.modify_data=od.date#时间
        #建立订单和商品的关系
        addorderlist = request.session.get('addorderlist', {})
        od.save()
        for com in addorderlist.values(): 
          oi=OInclude()
          oi.order=od
          comm=Commodity.objects.get(id=com["id"])
          oi.commodity=comm
          oi.quantity=com["quantity"]
          if od.type == "1":                    
            oi.amount=com["quantity"]*float(com["unitprice"])#不同订单金额计算方式不同
            inv=Inventory.objects.get(commodity=comm)#找到对应库存单
            print(inv.quantity)
            inv.quantity=inv.quantity-decimal.Decimal(oi.quantity)#销售单减去商品
            print(inv.quantity)
            inv.amount=inv.amount-decimal.Decimal(oi.amount)#减去金额
            war=inv.warehouse#找到相应仓库
            war.total=war.total-decimal.Decimal(oi.amount)#库存金额更新
            inv.save()
            war.save()
          else:
            oi.amount=com["quantity"]*float(com["costprice"])
            inv=Inventory.objects.get(commodity=comm)#找到对应库存单
            inv.quantity=inv.quantity+decimal.Decimal(oi.quantity)#供货单加上商品
            inv.amount=inv.amount+decimal.Decimal(oi.amount)#增加金额
            war=inv.warehouse#找到相应仓库
            war.total=war.total+decimal.Decimal(oi.amount)#库存金额更新
            inv.save()
            war.save()
          oi.type=request.session["ordertype"]
          oi.save()#储存数据
        eo.save()#储存数据
        cs.save()#储存数据
        del request.session['addorderlist']  
        del request.session['total_money']
        return HttpResponse("Y")
        
    except Exception as err:
        print(err)
        context = {"info":"订单添加失败，请稍后再试！"}
        return HttpResponse("N")

def corpfillter(request):
  ordertype = request.GET.get("type")
  request.session['ordertype'] = ordertype#放到session中
  corp=Corporation.objects.filter(cor_type=ordertype)#得到相应类型的往来单位
  corplist=dict()
  for c in corp:
    corplist[c.id]=c.toDict()
  request.session['corplist'] =corplist#放到session中
  return  redirect(reverse('addorder_index', args=[1]))