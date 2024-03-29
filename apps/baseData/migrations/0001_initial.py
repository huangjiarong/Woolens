# Generated by Django 2.0 on 2019-04-02 10:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ancillaryData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=120, verbose_name='账户编号')),
                ('name', models.CharField(max_length=120, verbose_name='账户名称')),
                ('cur_balance', models.FloatField(blank=True, null=True, verbose_name='当前余额')),
                ('pre_balance', models.FloatField(blank=True, null=True, verbose_name='期初余额')),
                ('type', models.CharField(blank=True, max_length=120, null=True, verbose_name='账户类别')),
                ('if_default', models.BooleanField(default=True, verbose_name='是否为默认账户')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=120, verbose_name='客户编号')),
                ('name', models.CharField(max_length=120, verbose_name='客户名称')),
                ('address', models.CharField(blank=True, max_length=120, null=True, verbose_name='地址')),
                ('link_man', models.CharField(blank=True, max_length=120, null=True, verbose_name='联系人')),
                ('telephone', models.CharField(blank=True, max_length=120, null=True, verbose_name='联系电话')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('fax', models.CharField(blank=True, max_length=120, null=True, verbose_name='传真')),
                ('credit_limit', models.IntegerField(blank=True, null=True, verbose_name='授信额度')),
                ('payment', models.CharField(blank=True, max_length=120, null=True, verbose_name='付款方式')),
                ('tr_num', models.CharField(blank=True, max_length=120, null=True, verbose_name='纳税人识别号')),
                ('pre_receivable', models.FloatField(blank=True, null=True, verbose_name='期初预收款')),
                ('receivable', models.FloatField(blank=True, null=True, verbose_name='期初应收款')),
                ('balance_date', models.DateField(verbose_name='余额日期')),
                ('deposit_bank', models.CharField(blank=True, max_length=120, null=True, verbose_name='开户银行')),
                ('account', models.CharField(blank=True, max_length=120, null=True, verbose_name='银行帐号')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ancillaryData.ClientType', verbose_name='客户类别')),
            ],
            options={
                'verbose_name': '客户表',
                'verbose_name_plural': '客户表',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120, verbose_name='用户名')),
                ('number', models.CharField(max_length=120, verbose_name='工号')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='真名')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('telephone', models.CharField(blank=True, max_length=12, null=True, verbose_name='手机')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='固定电话')),
                ('login_times', models.PositiveIntegerField(blank=True, null=True, verbose_name='登录次数')),
                ('department', models.CharField(blank=True, max_length=120, null=True, verbose_name='部门')),
                ('role', models.CharField(blank=True, max_length=120, null=True, verbose_name='角色')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
                ('operate', models.CharField(blank=True, max_length=120, null=True, verbose_name='操作')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=120, verbose_name='仓库编号')),
                ('name', models.CharField(max_length=120, verbose_name='仓库名')),
                ('department', models.CharField(blank=True, max_length=120, null=True, verbose_name='所属部门')),
                ('if_forbidden', models.BooleanField(default=False, verbose_name='是否禁用')),
                ('if_default', models.BooleanField(default=False, verbose_name='是否默认')),
                ('address', models.CharField(blank=True, max_length=120, null=True, verbose_name='地址')),
                ('area', models.FloatField(verbose_name='面积')),
                ('link_man', models.CharField(blank=True, max_length=120, null=True, verbose_name='联系人')),
                ('phone', models.CharField(blank=True, max_length=120, null=True, verbose_name='联系电话')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('type', models.ManyToManyField(related_name='warehouse', to='ancillaryData.WarehouseType', verbose_name='仓库类别')),
            ],
            options={
                'verbose_name': '仓库',
                'verbose_name_plural': '仓库',
            },
        ),
        migrations.CreateModel(
            name='Woolens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='毛料名称')),
                ('number', models.CharField(blank=True, max_length=120, null=True, verbose_name='编号')),
                ('abbreviation', models.CharField(blank=True, max_length=120, null=True, verbose_name='简称')),
                ('element', models.CharField(blank=True, max_length=120, null=True, verbose_name='成分')),
                ('cost', models.FloatField(default=0, verbose_name='色纱成本')),
                ('price', models.FloatField(default=0, verbose_name='色纱售价')),
                ('clerk', models.CharField(blank=True, max_length=120, null=True, verbose_name='录入人')),
                ('dyelot_num', models.CharField(blank=True, max_length=120, verbose_name='缸号')),
                ('batch_num', models.CharField(blank=True, max_length=120, verbose_name='批号')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ancillaryData.Color', verbose_name='颜色')),
                ('packaging', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ancillaryData.Packaging', verbose_name='包装')),
                ('type', models.ForeignKey(on_delete=True, to='ancillaryData.WoolensType', verbose_name='毛料类型')),
            ],
            options={
                'verbose_name': '毛料品种管理',
                'verbose_name_plural': '毛料品种管理',
            },
        ),
        migrations.AlterUniqueTogether(
            name='woolens',
            unique_together={('name', 'packaging', 'color', 'dyelot_num', 'batch_num')},
        ),
    ]
