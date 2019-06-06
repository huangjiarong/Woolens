from datetime import datetime

from django.db import models

from ancillaryData.models import Packaging
from warehouse_management.models import Inventory
from baseData.models import Warehouse, Client, Color


#打毛领料表
class Hairing(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    dye_goods = models.ForeignKey(Inventory, verbose_name='染色产品', on_delete=models.CASCADE)
    number = models.FloatField(verbose_name='数量')
    piece = models.FloatField(verbose_name='件数', blank=True, null=True)
    price = models.FloatField(verbose_name='成本单价')
    total_price = models.FloatField(verbose_name='总价')
    process = models.ForeignKey(Client, verbose_name='打毛厂', on_delete=models.CASCADE)
    ord_date = models.DateField(verbose_name='领料日期')
    return_date = models.DateField(verbose_name='预计回毛日期')
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    complete_return = models.BooleanField(verbose_name='是否回毛完成', default=False, blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '打毛领料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ord_num


#打毛回毛表
class HairingReturn(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    hairing = models.ManyToManyField(Hairing, verbose_name='所属打毛领料单号', related_name='hairing_return')
    name = models.CharField(verbose_name='品种', max_length=120)
    packaging = models.ForeignKey(Packaging, verbose_name='包装', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='颜色', on_delete=models.CASCADE)
    dyelot_num = models.CharField(verbose_name='缸号', max_length=120,blank=True)
    batch_num = models.CharField(verbose_name='批号', max_length=120,blank=True)
    number = models.FloatField(verbose_name='数量')
    piece = models.FloatField(verbose_name='件数', blank=True, null=True)
    price = models.FloatField(verbose_name='成本单价')
    total = models.FloatField(verbose_name='成本总额', default=0)
    assess_price = models.FloatField(verbose_name='评估单价', blank=True)
    actual_price = models.FloatField(verbose_name='实际单价', blank=True, null=True)
    A = models.FloatField(verbose_name='评估打毛回毛率', default=0.98, blank=True)
    A1 = models.FloatField(verbose_name='实际打毛回毛率', default=0.0, blank=True)
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
        verbose_name = '打毛回毛'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ord_num
