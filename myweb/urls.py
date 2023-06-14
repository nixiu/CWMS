from django.urls import path
from myweb.views import client, index,employee,commodity,warehouse,suppliers,addorder,sale,purchase

urlpatterns = [
    path('', index.index,name='index'),
    # 后台管理员路由
    path('login', index.login, name="myweb_login"),
    path('dologin', index.dologin, name="myweb_dologin"),
    path('logout', index.logout, name="myweb_logout"),
    
    #员工账号管理
    path('employee/<int:pIndex>', employee.index, name='employee_index'),  # 浏览
    path('employee/add', employee.add, name='employee_add'),  # 添加表单
    path('employee/insert', employee.insert, name='employee_insert'),  # 执行添加
    path('employee/del/<int:uid>', employee.delete, name='employee_del'),  # 执行删除
    path('employee/edit/<int:uid>', employee.edit, name='employee_edit'),  # 加载编辑表单
    path('employee/update/<int:uid>', employee.update, name='employee_update'),  # 执行编辑

    #商品管理
    path('commodity/<int:pIndex>', commodity.index, name='commodity_index'),  # 浏览
    path('commodity/add', commodity.add, name='commodity_add'),  # 添加表单
    path('commodity/insert', commodity.insert, name='commodity_insert'),  # 执行添加
    path('commodity/del/<int:uid>', commodity.delete, name='commodity_del'),  # 执行删除
    path('commodity/edit/<int:uid>', commodity.edit, name='commodity_edit'),  # 加载编辑表单
    path('commodity/update/<int:uid>', commodity.update, name='commodity_update'),  # 执行编辑

    #仓库管理
    path('warehouse/<int:pIndex>', warehouse.index, name='warehouse_index'),  # 浏览
    path('warehouse/add', warehouse.add, name='warehouse_add'),  # 添加表单
    path('warehouse/insert', warehouse.insert, name='warehouse_insert'),  # 执行添加
    path('warehouse/del/<int:uid>', warehouse.delete, name='warehouse_del'),  # 执行删除
    path('warehouse/edit/<int:uid>', warehouse.edit, name='warehouse_edit'),  # 加载编辑表单
    path('warehouse/update/<int:uid>', warehouse.update, name='warehouse_update'),  # 执行编辑

    #客户管理
    path('client/<int:pIndex>', client.index, name='client_index'),  # 浏览
    path('client/add', client.add, name='client_add'),  # 添加表单
    path('client/insert', client.insert, name='client_insert'),  # 执行添加
    path('client/del/<int:uid>', client.delete, name='client_del'),  # 执行删除
    path('client/edit/<int:uid>', client.edit, name='client_edit'),  # 加载编辑表单
    path('client/update/<int:uid>', client.update, name='client_update'),  # 执行编辑

    #供货商管理
    path('suppliers/<int:pIndex>', suppliers.index, name='suppliers_index'),  # 浏览
    path('suppliers/add', suppliers.add, name='suppliers_add'),  # 添加表单
    path('suppliers/insert', suppliers.insert, name='suppliers_insert'),  # 执行添加
    path('suppliers/del/<int:uid>', suppliers.delete, name='suppliers_del'),  # 执行删除
    path('suppliers/edit/<int:uid>', suppliers.edit, name='suppliers_edit'),  # 加载编辑表单
    path('suppliers/update/<int:uid>', suppliers.update, name='suppliers_update'),  # 执行编辑

    #添加订单管理
    path('addorder/<int:pIndex>', addorder.index, name='addorder_index'),  # 浏览
    # 订单信息管理路由
    path('addorder/add/<str:pid>', addorder.add, name='addorder_add'),
    path('addorder/delete/<str:pid>', addorder.delete, name='addorder_delete'),
    path('addorder/clear', addorder.clear, name='addorder_clear'),
    path('addorder/change', addorder.change, name='addorder_change'),
    path('addorder/insert', addorder.insert, name='addorder_insert'),    
    path('addorder/corpfillter', addorder.corpfillter, name='addorder_corpfillter'),

    #销售单
    path('sale/<int:pIndex>', sale.index, name='sale_index'),  # 浏览
    path('sale/del/<int:uid>', sale.delete, name='sale_del'),  # 执行删除
    path('sale/detail', sale.detail,name='sale_detail'), #订单的详情信息

    #进货单
    path('purchase/<int:pIndex>', purchase.index, name='purchase_index'),  # 浏览
    path('purchase/del/<int:uid>', purchase.delete, name='purchase_del'),  # 执行删除
    path('purchase/detail', purchase.detail,name='sale_detail'), #订单的详情信息

]