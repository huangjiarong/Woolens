from datetime import datetime

from django.db import models

from baseData.models import Warehouse, Client, Color
from ancillaryData.models import Packaging
from warehouse_management.models import Inventory


#染色领料表
class Dye(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    reeling = models.ForeignKey(Inventory, verbose_name='摇纱产品', on_delete=models.CASCADE)
    remain= models.FloatField(verbose_name='剩余数量', default=0)
    number = models.FloatField(verbose_name='数量')
    piece = models.FloatField(verbose_name='件数')
    prick_num = models.FloatField(verbose_name='扎数')
    price = models.FloatField(verbose_name='摇纱产品单价')
    total_price = models.FloatField(verbose_name='总价')
    process = models.ForeignKey(Client, verbose_name='染色厂', on_delete=models.CASCADE)
    ord_date = models.DateField(verbose_name='领料日期')
    opposite_num = models.CharField(verbose_name='对方单号', max_length=120)
    return_date = models.DateField(verbose_name='预计回毛日期')
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    complete_return = models.BooleanField(verbose_name='是否回毛完成', default=False, blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '染色领料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} - {}'.format(self.ord_num, self.reeling.name)


#染色通知
class DyeNotice(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    dye = models.ManyToManyField(Dye, verbose_name='所属染色领料', related_name='dye_notice')
    name = models.CharField(verbose_name='品种', max_length=120)
    packaging = models.ForeignKey(Packaging, verbose_name='包装', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='颜色', on_delete=models.CASCADE)
    dyelot_num = models.CharField(verbose_name='缸号', max_length=120, blank=True)
    batch_num = models.CharField(verbose_name='批号', max_length=120, blank=True)
    number = models.FloatField(verbose_name='数量')
    price = models.FloatField(verbose_name='单价')
    piece = models.FloatField(verbose_name='件数')
    prick_num = models.FloatField(verbose_name='扎数')
    ord_date = models.DateField(verbose_name='通知日期')
    dye_color = models.ForeignKey(Color, verbose_name='染色种类', on_delete=models.CASCADE, related_name='dye_color')
    return_date = models.DateField(verbose_name='预计回毛日期')
    complete_return = models.BooleanField(verbose_name='是否回毛完成', default=False, blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '染色通知'
        verbose_name_plural = verbose_name


#染色回毛
class DyeReturn(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    dye_notice = models.ManyToManyField(DyeNotice, verbose_name='所属染色通知单', related_name='dye_return')
    name = models.CharField(verbose_name='品种', max_length=120)
    packaging = models.ForeignKey(Packaging, verbose_name='包装', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='颜色', on_delete=models.CASCADE)
    dyelot_num = models.CharField(verbose_name='缸号', max_length=120,blank=True)
    batch_num = models.CharField(verbose_name='批号', max_length=120)
    number = models.FloatField(verbose_name='数量')
    piece = models.FloatField(verbose_name='件数')
    price = models.FloatField(verbose_name='摇纱产品单价')
    total = models.FloatField(verbose_name='摇纱产品总额', default=0)
    assess_price = models.FloatField(verbose_name='评估单价', blank=True)
    actual_price = models.FloatField(verbose_name='实际单价', blank=True, null=True)
    A = models.FloatField(verbose_name='评估染色回毛率', default=0.98, blank=True)
    A1 = models.FloatField(verbose_name='实际染色回毛率', default=0.0, blank=True)
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
        verbose_name = '染色回毛'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ord_num


