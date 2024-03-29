# Generated by Django 2.0 on 2019-04-02 10:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=120, verbose_name='编号')),
                ('name', models.CharField(max_length=120, verbose_name='类别名称')),
                ('pre_type', models.CharField(blank=True, max_length=120, null=True, verbose_name='上级类别')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '客户类别表',
                'verbose_name_plural': '客户类别表',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=30, verbose_name='颜色')),
                ('color_num', models.CharField(max_length=30, verbose_name='色号')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '颜色表',
                'verbose_name_plural': '颜色表',
            },
        ),
        migrations.CreateModel(
            name='Packaging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='类别名')),
                ('number', models.CharField(max_length=30, verbose_name='类别编号')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '包装类别',
                'verbose_name_plural': '包装类别',
            },
        ),
        migrations.CreateModel(
            name='WarehouseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='类别名')),
                ('number', models.CharField(max_length=30, verbose_name='类别编号')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '仓库类别表',
                'verbose_name_plural': '仓库类别表',
            },
        ),
        migrations.CreateModel(
            name='WoolensType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=120, verbose_name='类别编号')),
                ('name', models.CharField(max_length=120, verbose_name='类别名称')),
                ('pre_type', models.CharField(blank=True, max_length=120, null=True, verbose_name='上级类别')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('remarks', models.CharField(blank=True, max_length=120, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '产品类别表',
                'verbose_name_plural': '产品类别表',
            },
        ),
    ]
