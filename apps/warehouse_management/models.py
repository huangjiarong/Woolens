from datetime import datetime

from django.db import models

from baseData.models import Warehouse
from ancillaryData.models import Color, Packaging


WOOLENS_TYPE_CHOICE = (
    ('原材料', '原材料'),
    ('摇纱产品', '摇纱产品'),
    ('拼纱产品', '拼纱产品'),
    ('染色产品', '染色产品'),
    ('打毛产品', '打毛产品'),
)
#库存表
class Inventory(models.Model):
    name = models.CharField(verbose_name='品种', max_length=120)
    packaging = models.ForeignKey(Packaging, verbose_name='包装', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='颜色', on_delete=models.CASCADE)
    dyelot_num = models.CharField(verbose_name='缸号', max_length=120)
    batch_num = models.CharField(verbose_name='批号', max_length=120)
    woolens_type = models.CharField(verbose_name='毛料类型', choices=WOOLENS_TYPE_CHOICE,
                                    max_length=120, default='原材料')
    number = models.FloatField(verbose_name='数量',null=True)
    assess_price = models.FloatField(verbose_name='评估单价',null=True)
    actual_price = models.FloatField(verbose_name='实际单价',null=True)
    warehouse = models.ForeignKey(Warehouse, verbose_name='仓库', on_delete=models.CASCADE, related_name='inventory')
    create_people = models.CharField(verbose_name='制单人', max_length=120,null=True, blank=True)
    create_date = models.DateField(verbose_name='制单时间',default=datetime.now)
    check_status = models.BooleanField(verbose_name='审核状态',default=False, blank=True)
    check_people = models.CharField(verbose_name='审核人', max_length=120,null=True)
    check_date = models.DateField(verbose_name='审核时间',default=datetime.now)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '库存表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} - {} - {}'.format(self.name, self.woolens_type, self.warehouse.name)


#调拨
class Transfers(models.Model):
    ord_num = models.CharField(max_length=120, verbose_name='调拨单号')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name='库存')
    transfers_num = models.FloatField(verbose_name='调拨数量')
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='调出仓库',
                                       related_name='from_warehouse')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='调入仓库',
                                       related_name='to_warehouse')
    date = models.DateField(verbose_name='调拨日期')
    remarks = models.CharField(max_length=120, verbose_name='备注', blank=True, default="")
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '调拨单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ord_num


#盘点
class Check(models.Model):
    ord_num = models.CharField(max_length=120, verbose_name='调拨单号')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='仓库')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name='库存')
    number = models.FloatField(verbose_name='系统数量')
    actual_num = models.FloatField(verbose_name='实际数量')
    difference = models.FloatField(verbose_name='盈亏数量')
    date = models.DateField(verbose_name='盘点日期')
    remarks = models.CharField(max_length=120, verbose_name='备注', blank=True, default="")
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '盘点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ord_num
