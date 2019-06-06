# Generated by Django 2.0 on 2019-04-02 10:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('baseData', '0001_initial'),
        ('ancillaryData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ord_num', models.CharField(max_length=120, verbose_name='订单号')),
                ('number', models.FloatField(verbose_name='购货数量')),
                ('price', models.FloatField(verbose_name='购货单价')),
                ('total', models.FloatField(verbose_name='购货总额')),
                ('tax_price', models.FloatField(verbose_name='含税单价')),
                ('tax_total', models.FloatField(verbose_name='税额')),
                ('sum', models.FloatField(verbose_name='采购费用')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='购货日期')),
                ('remarks', models.CharField(blank=True, max_length=120, verbose_name='备注')),
                ('source_orderNum', models.CharField(max_length=120, verbose_name='源单号')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Client', verbose_name='供应商')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Warehouse', verbose_name='入库仓库')),
                ('woolens', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Woolens', verbose_name='毛料')),
            ],
            options={
                'verbose_name': '购货单',
                'verbose_name_plural': '购货单',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ord_num', models.CharField(max_length=120, verbose_name='订单号')),
                ('number', models.FloatField(verbose_name='订货数量')),
                ('price', models.FloatField(verbose_name='订货单价')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='订货总额')),
                ('preorder_num', models.FloatField(verbose_name='可赊数量')),
                ('preorder_price', models.FloatField(verbose_name='赊货单价')),
                ('preorder_total', models.FloatField(verbose_name='赊货总额')),
                ('tax_price', models.FloatField(blank=True, null=True, verbose_name='含税单价')),
                ('tax_total', models.FloatField(blank=True, null=True, verbose_name='税额')),
                ('order_date', models.DateField(default=datetime.datetime.now, verbose_name='订购日期')),
                ('delivery_date', models.DateField(verbose_name='交货日期')),
                ('deadline', models.DateField(verbose_name='最晚取货日期')),
                ('check_status', models.BooleanField(default=False, verbose_name='审核状态')),
                ('complete_return', models.BooleanField(default=False, verbose_name='是否取货完成')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
                ('remain', models.FloatField(blank=True, default=0, verbose_name='剩余数量')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Client', verbose_name='供应商')),
                ('woolens', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Woolens', verbose_name='毛料')),
            ],
            options={
                'verbose_name': '购货订单',
                'verbose_name_plural': '购货订单',
            },
        ),
        migrations.CreateModel(
            name='TakeGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ord_num', models.CharField(max_length=120, verbose_name='单号')),
                ('opposite_num', models.CharField(default=' ', max_length=60, verbose_name='对方单号')),
                ('name', models.CharField(default='', max_length=120, verbose_name='毛料')),
                ('dyelot_num', models.CharField(blank=True, max_length=120, null=True, verbose_name='缸号')),
                ('batch_num', models.CharField(blank=True, max_length=120, null=True, verbose_name='批号')),
                ('take_num', models.FloatField(verbose_name='取货数量')),
                ('take_price', models.FloatField(verbose_name='取货单价')),
                ('take_total', models.FloatField(verbose_name='取货总额')),
                ('take_people', models.CharField(blank=True, max_length=120, null=True, verbose_name='取货人')),
                ('take_date', models.DateField(default=datetime.datetime.now, verbose_name='取货日期')),
                ('complete_return', models.BooleanField(default=False, verbose_name='是否回毛完成')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ancillaryData.Color', verbose_name='颜色')),
                ('packaging', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ancillaryData.Packaging', verbose_name='包装')),
                ('purchase_order', models.ManyToManyField(related_name='take_goods', to='purchase.PurchaseOrder', verbose_name='所属购货订单')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Warehouse', verbose_name='入库仓库')),
            ],
            options={
                'verbose_name': '取货表',
                'verbose_name_plural': '取货表',
            },
        ),
    ]
