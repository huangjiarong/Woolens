from datetime import datetime

from django.db import models

from ancillaryData.models import ClientType, WoolensType, Color, WarehouseType,\
    Packaging


#客户表
class Client(models.Model):
    number = models.CharField(verbose_name='客户编号', max_length=120)
    name = models.CharField(verbose_name='客户名称', max_length=120)
    address =models.CharField(verbose_name='地址', max_length=120, blank=True, null=True)
    link_man = models.CharField(verbose_name='联系人', max_length=120, blank=True, null=True)
    telephone = models.CharField(verbose_name='联系电话', max_length=120, blank=True, null=True)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)
    fax = models.CharField(verbose_name='传真', max_length=120, blank=True, null=True)
    credit_limit = models.IntegerField(verbose_name='授信额度', blank=True, null=True)
    payment = models.CharField(verbose_name='付款方式', max_length=120, blank=True, null=True)
    type = models.ManyToManyField(ClientType, verbose_name='客户类别')
    tr_num = models.CharField(verbose_name='纳税人识别号', max_length=120, blank=True, null=True)
    pre_receivable = models.FloatField(verbose_name='期初预收款', default=0, blank=True)
    receivable = models.FloatField(verbose_name='期初应收款', blank=True, default=0)
    balance_date = models.DateField(verbose_name='余额日期')
    deposit_bank = models.CharField(verbose_name='开户银行', max_length=120, blank=True, null=True)
    account = models.CharField(verbose_name='银行帐号', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户表'
        verbose_name_plural = verbose_name
        unique_together = ('name', )


#毛料品种管理表
class Woolens(models.Model):
    name = models.CharField(verbose_name='毛料名称', max_length=120)
    type = models.ForeignKey(WoolensType, verbose_name='毛料类型', on_delete=True)
    number = models.CharField(verbose_name='编号', max_length=120, blank=True, null=True)
    abbreviation = models.CharField(verbose_name='简称', max_length=120, blank=True, null=True)
    element = models.CharField(verbose_name='成分',max_length=120, blank=True, null=True)
    cost = models.FloatField(verbose_name='色纱成本', default=0)
    price = models.FloatField(verbose_name='色纱售价', default=0)
    clerk = models.CharField(verbose_name='录入人', max_length=120, blank=True, null=True)
    packaging = models.ForeignKey(Packaging, verbose_name='包装', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='颜色', on_delete=models.CASCADE)
    dyelot_num = models.CharField(verbose_name='缸号', max_length=120, blank=True)
    batch_num = models.CharField(verbose_name='批号', max_length=120, blank=True)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '毛料品种管理'
        verbose_name_plural = verbose_name
        unique_together = ('name', 'packaging', 'color', 'dyelot_num', 'batch_num')

#仓库表
class Warehouse(models.Model):
    number = models.CharField(verbose_name='仓库编号', max_length=120)
    name = models.CharField(verbose_name='仓库名', max_length=120)
    type = models.ManyToManyField(WarehouseType, verbose_name='仓库类别', related_name='warehouse')
    department = models.CharField(verbose_name='所属部门', max_length=120, blank=True, null=True)
    if_forbidden = models.BooleanField(verbose_name='是否禁用', default=False)
    if_default = models.BooleanField(verbose_name='是否默认', default=False)
    address = models.CharField(verbose_name='地址', max_length=120, blank=True, null=True)
    area = models.FloatField(verbose_name='面积')
    link_man = models.CharField(verbose_name='联系人', max_length=120, blank=True, null=True)
    phone = models.CharField(verbose_name='联系电话', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = verbose_name
        unique_together = ('name', )

    def __str__(self):
        return self.name


#员工表
class Staff(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=120)
    number = models.CharField(verbose_name='工号', max_length=120)
    name = models.CharField(verbose_name='真名', max_length=120, blank=True, null=True)
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)
    telephone = models.CharField(verbose_name='手机', max_length=12, blank=True, null=True)
    phone = models.CharField(verbose_name='固定电话', max_length=20, blank=True, null=True)
    login_times = models.PositiveIntegerField(verbose_name='登录次数', blank=True, null=True)
    department = models.CharField(verbose_name='部门', max_length=120, blank=True, null=True)
    role = models.CharField(verbose_name='角色', max_length=120, blank=True, null=True)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    operate = models.CharField(verbose_name='操作', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    class Meta:
        verbose_name = '员工'
        verbose_name_plural = verbose_name
        unique_together = ('username', )

    def __str__(self):
        return self.name

#账户管理
class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='所属客户', related_name='account_client')
    number = models.CharField(verbose_name='账户编号', max_length=120)
    name = models.CharField(verbose_name='账户名称', max_length=120)
    cur_balance = models.FloatField(verbose_name='当前余额', blank=True, null=True)
    pre_balance = models.FloatField(verbose_name='期初余额', blank=True, null=True)
    type = models.CharField(verbose_name='账户类别', max_length=120, blank=True, null=True)
    if_default = models.BooleanField(verbose_name='是否为默认账户', default=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = verbose_name
        unique_together = ('name', 'client', )

    def __str__(self):
        return self.name
