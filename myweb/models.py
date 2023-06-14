# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `#managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import decimal

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.CASCADE)
    permission = models.ForeignKey('AuthPermission', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.CASCADE)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    group = models.ForeignKey(AuthGroup, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    permission = models.ForeignKey(AuthPermission, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Commodity(models.Model):
    name = models.CharField(max_length=20)
    unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    costprice = models.DecimalField(max_digits=10, decimal_places=2)
    def toDict(self):
        unitprice=str(decimal.Decimal(self.unitprice).quantize(decimal.Decimal('0.00')))
        costprice=str(decimal.Decimal(self.costprice).quantize(decimal.Decimal('0.00')))
        return {'id':self.id, 'name':self.name, 'unitprice':unitprice,  'costprice':costprice}
    class Meta:
        db_table = 'commodity'


class CorSubmit(models.Model):
    date = models.DateTimeField()
    order = models.ForeignKey('Orders', models.CASCADE, db_column='or_id', blank=True, null=True)
    cor = models.ForeignKey('Corporation', models.CASCADE)

    class Meta:
        db_table = 'cor_submit'


class Corporation(models.Model):
    cor_name = models.CharField(max_length=20)
    cor_address = models.CharField(max_length=30)
    cor_type = models.IntegerField()
    cor_phone = models.CharField(max_length=11)
    cor_contact=models.CharField(max_length=10)
    def toDict(self):
        return {'id':self.id, 'cor_name':self.cor_name, 'cor_addresss':self.cor_address,'cor_type':self.cor_type,
        'cor_phone':self.cor_phone,'cor_contact':self.cor_contact}
    class Meta:
        db_table = 'corporation'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EmOrder(models.Model):
    em = models.OneToOneField('Employee', models.CASCADE, primary_key=True)
    or_field = models.ForeignKey('Orders', models.CASCADE, db_column='or_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    modify_data = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'em_order'



class Employee(models.Model):
    name = models.CharField(max_length=20)
    type = models.IntegerField()
    phone = models.CharField(max_length=11)
    user_name = models.CharField(max_length=20)
    password_hash = models.CharField(max_length=128)  # 密码
    password_salt = models.CharField(max_length=128)  # 密码干扰值
    def toDict(self):
        return {'id':self.id, 'user_name':self.user_name, 'name':self.name, 'password_hash':self.password_hash, 'password_salt':self.password_salt, 'type':self.type, 'phone':self.phone}
    class Meta:
        db_table = 'employee'


class Inventory(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    commodity = models.ForeignKey(Commodity, models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', models.CASCADE)

    class Meta:
        db_table = 'inventory'

class Orders(models.Model):
    illustrate = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10)
    date =models.DateTimeField()
    total=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'orders'

class OInclude(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity =models.DecimalField(max_digits=10, decimal_places=2)
    commodity = models.ForeignKey(Commodity, models.CASCADE)
    order = models.ForeignKey(Orders, models.CASCADE)
    type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'o_include'





class Warehouse(models.Model):
    name = models.CharField(max_length=20)
    explorer = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    total=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'warehouse'
