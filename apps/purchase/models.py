from datetime import datetime

from django.db import models

from ancillaryData.models import Packaging
from baseData.models import WoolensType, Warehouse, Woolens, Client
from ancillaryData.models import Color


#购货订单
class PurchaseOrder(models.Model):
    ord_num = models.CharField(verbose_name='订单号', max_length=120)
    woolens = models.ForeignKey(Woolens, verbose_name='毛料', on_delete=models.CASCADE)
    number = models.FloatField(verbose_name='订货数量')
    price = models.FloatField(verbose_name='订货单价')
    total = models.FloatField(verbose_name='订货总额', blank=True, null=True)
    preorder_num = models.FloatField(verbose_name='可赊数量')
    preorder_price = models.FloatField(verbose_name='赊货单价')
    preorder_total = models.FloatField(verbose_name='赊货总额')
    tax_price = models.FloatField(verbose_name='含税单价', blank=True, null=True)
    tax_total = models.FloatField(verbose_name='税额', blank=True, null=True)
    supplier = models.ForeignKey(Client, verbose_name='供应商', on_delete=models.CASCADE)
    order_date = models.DateField(verbose_name='订购日期', default=datetime.now)
    delivery_date = models.DateField(verbose_name='交货日期')
    deadline = models.DateField(verbose_name='最晚取货日期')
    check_status = models.BooleanField(verbose_name='审核状态', default=False, blank=True)
    complete_return = models.BooleanField(verbose_name='是否取货完成', default=False, blank=True)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    remain = models.FloatField(verbose_name='剩余数量', blank=True, default=0)

    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return '{} -- {}'.format(self.ord_num, self.woolens)

    class Meta:
        verbose_name = '购货订单'
        verbose_name_plural = verbose_name
        # unique_together = ('number', 'materialName')


#取货表
class TakeGoods(models.Model):
    purchase_order = models.ManyToManyField(PurchaseOrder, verbose_name='所属购货订单',  related_name='take_goods')
    ord_num = models.CharField(verbose_name='单号', max_length=120)
    opposite_num = models.CharField(verbose_name='对方单号', default=' ', max_length=60)
    name = models.CharField(verbose_name='毛料', max_length=120,default='')
    color = models.ForeignKey(Color, verbose_name='颜色', on_delete=models.CASCADE)
    dyelot_num = models.CharField(verbose_name='缸号', max_length=120, blank=True, null=True)
    batch_num = models.CharField(verbose_name='批号', max_length=120, blank=True, null=True)
    packaging = models.ForeignKey(Packaging, verbose_name='包装', on_delete=models.CASCADE)
    take_num = models.FloatField(verbose_name='取货数量')
    take_price = models.FloatField(verbose_name='取货单价')
    take_total = models.FloatField(verbose_name='取货总额')
    take_people = models.CharField(verbose_name='取货人', max_length=120, blank=True, null=True)
    take_date = models.DateField(verbose_name='取货日期', default=datetime.now)
    warehouse = models.ForeignKey(Warehouse, verbose_name='入库仓库', on_delete=models.CASCADE)
    complete_return = models.BooleanField(verbose_name='是否回毛完成', default=False, blank=True)
    remarks = models.CharField(max_length=120, verbose_name='备注', blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '取货表'
        verbose_name_plural = verbose_name

#购货单
class Purchase(models.Model):
    ord_num = models.CharField(verbose_name='订单号', max_length=120)
    woolens = models.ForeignKey(Woolens, verbose_name='毛料', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Client, verbose_name='供应商', on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, verbose_name='入库仓库', on_delete=models.CASCADE)
    number = models.FloatField(verbose_name='购货数量')
    price = models.FloatField(verbose_name='购货单价')
    total = models.FloatField(verbose_name='购货总额')
    tax_price = models.FloatField(verbose_name='含税单价')
    tax_total = models.FloatField(verbose_name='税额')
    sum = models.FloatField(verbose_name='采购费用')
    date = models.DateField(verbose_name='购货日期', default=datetime.now)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True)
    source_orderNum = models.CharField(verbose_name='源单号', max_length=120)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '购货单'
        verbose_name_plural = verbose_name


