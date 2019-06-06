from datetime import datetime

from django.db import models


#客户类别表
class ClientType(models.Model):
    number = models.CharField(verbose_name='编号', max_length=120)
    name = models.CharField(verbose_name='类别名称', max_length=120)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = '客户类别表'
        verbose_name_plural = verbose_name
        unique_together = ('name',)

    def __str__(self):
        return self.name


#产品类别表
class WoolensType(models.Model):
    number = models.CharField(verbose_name='类别编号', max_length=120)
    name = models.CharField(verbose_name='类别名称', max_length=120)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = '产品类别表'
        verbose_name_plural = verbose_name
        unique_together = ('name',)

    def __str__(self):
        return self.name


#颜色表
class Color(models.Model):
    color = models.CharField(verbose_name='颜色', max_length=30)
    color_num = models.CharField(verbose_name='色号', max_length=30)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = '颜色表'
        verbose_name_plural = verbose_name
        unique_together = ('color', 'color_num', )


#仓库类别表
class WarehouseType(models.Model):
    name = models.CharField(verbose_name='类别名', max_length=30)
    number = models.CharField(verbose_name='类别编号', max_length=30)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '仓库类别表'
        verbose_name_plural = verbose_name
        unique_together = ('name',)


#包装类别
class Packaging(models.Model):
    name = models.CharField(verbose_name='类别名', max_length=30)
    number = models.CharField(verbose_name='类别编号', max_length=30)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '包装类别'
        verbose_name_plural = verbose_name
        unique_together = ('name',)


#结算方式
class Settlement(models.Model):
    name = models.CharField(verbose_name='结算方式', max_length=30)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '结算方式'
        verbose_name_plural = verbose_name
        unique_together = ('name',)
