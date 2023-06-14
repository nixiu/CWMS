from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import hashlib
from myweb.models import Employee,Warehouse,Corporation,Orders
# Create your views here.

def index(request):
  request.session['ordertype']=1
  cor=Corporation.objects.all()
  corlen=len(cor)
  
  war=Warehouse.objects.all()
  warcount=0
  for i in war:
    warcount+=warcount+i.total
  ors=Orders.objects.filter(type=1)
  orlen=len(ors)
  context={"corlen":corlen,"warcount":warcount,"orlen":orlen}
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
