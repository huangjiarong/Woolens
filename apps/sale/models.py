from datetime import datetime

from django.db import models

from warehouse_management.models import Inventory
from baseData.models import Client, Account, Staff


#销售单
class Sale(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=60)
    woolens = models.ForeignKey(Inventory, verbose_name='毛料', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='客户', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, verbose_name='结算账户', on_delete=models.CASCADE)
    staff = models.CharField(verbose_name='销售人员', max_length=60)
    sale_num = models.FloatField(verbose_name='销售数量')
    sale_price = models.FloatField(verbose_name='销售单价')
    sale_total = models.FloatField(verbose_name='销售总价')
    book_num = models.FloatField(verbose_name='预订数量')
    book_price = models.FloatField(verbose_name='预订单价')
    book_total = models.FloatField(verbose_name='预订总价')
    tax_price = models.FloatField(verbose_name='含税单价')
    tax_total = models.FloatField(verbose_name='含税总价')
    count = models.FloatField(verbose_name='价税合计')
    ord_date = models.DateField(verbose_name='单据日期')
    take_date = models.DateField(verbose_name='交货日期')
    proceeds = models.FloatField(verbose_name='本次收款')
    arrear = models.FloatField(verbose_name='本次欠款')
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.ord_num

    class Meta:
        verbose_name = '销售单'
        verbose_name_plural = verbose_name


#销售订单
class SaleOrder(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=60)
    woolens = models.ForeignKey(Inventory, verbose_name='毛料', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='客户', on_delete=models.CASCADE)
    staff = models.CharField(verbose_name='销售人员', max_length=60)
    sale_num = models.FloatField(verbose_name='销售数量')
    sale_price = models.FloatField(verbose_name='销售单价')
    sale_total = models.FloatField(verbose_name='销售总价')
    book_num = models.FloatField(verbose_name='预订数量')
    book_price = models.FloatField(verbose_name='预订单价')
    book_total = models.FloatField(verbose_name='预订总价')
    tax_price = models.FloatField(verbose_name='含税单价')
    tax_total = models.FloatField(verbose_name='含税总价')
    count = models.FloatField(verbose_name='价税合计')
    proceeds = models.FloatField(verbose_name='本次收款')
    remain = models.FloatField(verbose_name='剩余数量')
    ord_date = models.DateField(verbose_name='单据日期')
    take_date = models.DateField(verbose_name='交货日期')
    deadline = models.DateField(verbose_name='最晚取货日期')
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.ord_num

    class Meta:
        verbose_name = '销售订单'
        verbose_name_plural = verbose_name


#销售出货单
class SaleExport(models.Model):
    ord_num = models.CharField(verbose_name='单号', max_length=60)
    sale_order = models.ForeignKey(SaleOrder, verbose_name='所属销售订单', on_delete=models.CASCADE)
    staff = models.CharField(verbose_name='负责员工', max_length=60)
    ord_date = models.DateField(verbose_name='出库时间')
    take_num = models.FloatField(verbose_name='取货数量')
    take_price = models.FloatField(verbose_name='取货单价')
    take_total = models.FloatField(verbose_name='取货总价')
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.ord_num

    class Meta:
        verbose_name = '销售出货单'
        verbose_name_plural = verbose_name
