from datetime import datetime

from django.db import models

from ancillaryData.models import Packaging
from baseData.models import Warehouse, Client, Color
from warehouse_management.models import Inventory


#摇纱领料表
class Reeling(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    material = models.ForeignKey(Inventory, verbose_name='原材料', on_delete=models.CASCADE)
    number = models.FloatField(verbose_name='数量')
    piece = models.FloatField(verbose_name='件数', blank=True, null=True)
    price = models.FloatField(verbose_name='原材料单价')
    total_price = models.FloatField(verbose_name='总价')
    process = models.ForeignKey(Client, verbose_name='摇纱厂', on_delete=models.CASCADE)
    ord_date = models.DateField(verbose_name='领料日期')
    return_date = models.DateField(verbose_name='预计回毛日期')
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    complete_return = models.BooleanField(verbose_name='是否回毛完成', default=False, blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '摇纱领料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ord_num


#摇纱回毛表
class ReelingReturn(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    reeling = models.ManyToManyField(Reeling, verbose_name='所属摇纱领料单号', related_name='reeling_return')
    name = models.CharField(verbose_name='品种', max_length=120)
    packaging = models.ForeignKey(Packaging, verbose_name='包装', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='颜色', on_delete=models.CASCADE)
    dyelot_num = models.CharField(verbose_name='缸号', max_length=120,blank=True)
    batch_num = models.CharField(verbose_name='批号', max_length=120,blank=True)
    number = models.FloatField(verbose_name='数量')
    piece = models.FloatField(verbose_name='件数', blank=True, null=True)
    price = models.FloatField(verbose_name='原材料单价')
    total = models.FloatField(verbose_name='原材料总额', default=0)
    assess_price = models.FloatField(verbose_name='评估单价', blank=True)
    actual_price = models.FloatField(verbose_name='实际单价', blank=True, default=0)
    A = models.FloatField(verbose_name='评估摇纱回毛率', default=0.98, blank=True)
    A1 = models.FloatField(verbose_name='实际摇纱回毛率', default=0.0, blank=True)
    process_price = models.FloatField(verbose_name='加工价')
    process_total = models.FloatField(verbose_name='加工金额')
    total_price = models.FloatField(verbose_name='总额')
    return_date = models.DateField(verbose_name='回毛日期')
    opposite_num = models.CharField(verbose_name='对方单号', max_length=120)
    warehouse = models.ForeignKey(Warehouse, verbose_name='回毛仓库', on_delete=models.CASCADE)
    remarks = models.CharField(verbose_name='备注', max_length=120, null=True, blank=True)
    complete_return = models.BooleanField(verbose_name='是否回毛完成', default=False, blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '摇纱回毛'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ord_num
