# Generated by Django 3.2.16 on 2023-06-16 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('unitprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costprice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'commodity',
            },
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cor_name', models.CharField(max_length=20)),
                ('cor_address', models.CharField(max_length=30)),
                ('cor_type', models.IntegerField()),
                ('cor_phone', models.CharField(max_length=11)),
                ('cor_contact', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'corporation',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('type', models.IntegerField()),
                ('phone', models.CharField(max_length=11)),
                ('user_name', models.CharField(max_length=20)),
                ('password_hash', models.CharField(max_length=128)),
                ('password_salt', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('illustrate', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(max_length=10)),
                ('date', models.DateTimeField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('explorer', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'warehouse',
            },
        ),
        migrations.CreateModel(
            name='OInclude',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(blank=True, max_length=10, null=True)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.commodity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.orders')),
            ],
            options={
                'db_table': 'o_include',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.commodity')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.warehouse')),
            ],
            options={
                'db_table': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='CorSubmit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('cor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.corporation')),
                ('order', models.ForeignKey(blank=True, db_column='or_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='myweb.orders')),
            ],
            options={
                'db_table': 'cor_submit',
            },
        ),
        migrations.CreateModel(
            name='EmOrder',
            fields=[
                ('em', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myweb.employee')),
                ('modify_data', models.DateTimeField(blank=True, null=True)),
                ('or_field', models.ForeignKey(blank=True, db_column='or_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='myweb.orders')),
            ],
            options={
                'db_table': 'em_order',
            },
        ),
    ]