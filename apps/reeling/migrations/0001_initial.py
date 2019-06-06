# Generated by Django 2.0 on 2019-04-02 10:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouse_management', '0001_initial'),
        ('baseData', '0001_initial'),
        ('ancillaryData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reeling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ord_num', models.CharField(max_length=120, verbose_name='单号')),
                ('number', models.FloatField(verbose_name='数量')),
                ('piece', models.FloatField(blank=True, null=True, verbose_name='件数')),
                ('price', models.FloatField(verbose_name='原材料单价')),
                ('total_price', models.FloatField(verbose_name='总价')),
                ('ord_date', models.DateField(verbose_name='领料日期')),
                ('return_date', models.DateField(verbose_name='预计回毛日期')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
                ('complete_return', models.BooleanField(default=False, verbose_name='是否回毛完成')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse_management.Inventory', verbose_name='原材料')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Client', verbose_name='摇纱厂')),
            ],
            options={
                'verbose_name': '摇纱领料',
                'verbose_name_plural': '摇纱领料',
            },
        ),
        migrations.CreateModel(
            name='ReelingReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ord_num', models.CharField(max_length=120, verbose_name='单号')),
                ('name', models.CharField(max_length=120, verbose_name='品种')),
                ('dyelot_num', models.CharField(blank=True, max_length=120, verbose_name='缸号')),
                ('batch_num', models.CharField(blank=True, max_length=120, verbose_name='批号')),
                ('number', models.FloatField(verbose_name='数量')),
                ('piece', models.FloatField(blank=True, null=True, verbose_name='件数')),
                ('price', models.FloatField(verbose_name='原材料单价')),
                ('total', models.FloatField(default=0, verbose_name='原材料总额')),
                ('assess_price', models.FloatField(blank=True, verbose_name='评估单价')),
                ('actual_price', models.FloatField(blank=True, default=0, verbose_name='实际单价')),
                ('A', models.FloatField(blank=True, default=0.98, verbose_name='评估摇纱回毛率')),
                ('A1', models.FloatField(blank=True, default=0.0, verbose_name='实际摇纱回毛率')),
                ('process_price', models.FloatField(verbose_name='加工价')),
                ('process_total', models.FloatField(verbose_name='加工金额')),
                ('total_price', models.FloatField(verbose_name='总额')),
                ('return_date', models.DateField(verbose_name='回毛日期')),
                ('opposite_num', models.CharField(max_length=120, verbose_name='对方单号')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
                ('complete_return', models.BooleanField(default=False, verbose_name='是否回毛完成')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ancillaryData.Color', verbose_name='颜色')),
                ('packaging', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ancillaryData.Packaging', verbose_name='包装')),
                ('reeling', models.ManyToManyField(related_name='reeling_return', to='reeling.Reeling', verbose_name='所属摇纱领料单号')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseData.Warehouse', verbose_name='回毛仓库')),
            ],
            options={
                'verbose_name': '摇纱回毛',
                'verbose_name_plural': '摇纱回毛',
            },
        ),
    ]