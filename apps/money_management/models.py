from datetime import datetime

from django.db import models

from baseData.models import Client, Account
from ancillaryData.models import Settlement


BUSINESS_TYPE_CHOICE = (
    ('订货', '订货'),
    ('购货', '购货'),
    ('销货出货应收款', '销货出货应收款'),
    ('销货应收款', '销货应收款'),
    ('摇纱', '摇纱'),
    ('拼纱', '拼纱'),
    ('染色', '染色'),
    ('打毛', '打毛'),
)

#应付款
class Due(models.Model):
    ord_num = models.CharField(max_length=60, verbose_name='单号', null=True)
    source_ordNum = models.CharField(max_length=60, verbose_name='源单号')
    client = models.ForeignKey(Client, verbose_name='客户', on_delete=models.CASCADE,
                               related_name='due')
    business_type = models.CharField(max_length=60, verbose_name='业务类别', choices=BUSINESS_TYPE_CHOICE)
    date = models.DateField(verbose_name='单据日期', null=True)
    money = models.FloatField(verbose_name='单据金额', default=0)
    had_cancel = models.FloatField(verbose_name='已核销', default=0)
    not_cancel = models.FloatField(verbose_name='未核销', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.ord_num

    class Meta:
        verbose_name = '应付款'
        verbose_name_plural = verbose_name


#付款单
class Payment(models.Model):
    ord_num = models.CharField(max_length=60, verbose_name='单据编号')
    due = models.ManyToManyField(Due, verbose_name='对应应付款单', through='Payment_to_Due')
    client = models.ForeignKey(Client, verbose_name='客户', on_delete=models.CASCADE,
                               related_name='pay')
    payer = models.CharField(max_length=60, verbose_name='付款人')
    date = models.DateField(verbose_name='单据日期')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='结算账户')
    pay_money = models.FloatField(verbose_name='付款金额')
    settlement_type = models.ForeignKey(Settlement, on_delete=models.CASCADE, verbose_name='结算方式')
    settlement_num = models.CharField(verbose_name='结算号', max_length=30)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.ord_num

    class Meta:
        verbose_name = '付款单'
        verbose_name_plural = verbose_name


class Payment_to_Due(models.Model):
    payment = models.ForeignKey(Payment, verbose_name='付款单', on_delete=models.CASCADE)
    due = models.ForeignKey(Due, verbose_name='应付款', on_delete=models.CASCADE)
    cancel = models.FloatField(verbose_name='本次核销', default=0)

    class Meta:
        verbose_name = '应付款核销记录'
        verbose_name_plural = verbose_name


#应收款
class Account_Due(models.Model):
    ord_num = models.CharField(max_length=60, verbose_name='单号', null=True)
    source_ordNum = models.CharField(max_length=60, verbose_name='源单号')
    client = models.ForeignKey(Client, verbose_name='客户', on_delete=models.CASCADE,
                               related_name='account_due')
    business_type = models.CharField(max_length=60, verbose_name='业务类别', choices=BUSINESS_TYPE_CHOICE)
    date = models.DateField(verbose_name='单据日期', null=True)
    money = models.FloatField(verbose_name='单据金额', default=0)
    had_cancel = models.FloatField(verbose_name='已核销', default=0)
    not_cancel = models.FloatField(verbose_name='未核销', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.ord_num

    class Meta:
        verbose_name = '应收款'
        verbose_name_plural = verbose_name


#收款单
class Receipt(models.Model):
    ord_num = models.CharField(max_length=60, verbose_name='单据编号')
    account_due = models.ManyToManyField(Account_Due, verbose_name='对应应收款单', through='Receipt_to_AccountDue')
    client = models.ForeignKey(Client, verbose_name='客户', on_delete=models.CASCADE,
                               related_name='receipt')
    staff = models.CharField(max_length=60, verbose_name='收银人')
    date = models.DateField(verbose_name='单据日期')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='结算账户')
    receipt_money = models.FloatField(verbose_name='收款金额')
    settlement_type = models.ForeignKey(Settlement, on_delete=models.CASCADE, verbose_name='结算方式')
    settlement_num = models.CharField(verbose_name='结算号', max_length=30)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.ord_num

    class Meta:
        verbose_name = '收款单'
        verbose_name_plural = verbose_name


class Receipt_to_AccountDue(models.Model):
    receipt = models.ForeignKey(Receipt, verbose_name='收款单', on_delete=models.CASCADE)
    account_due = models.ForeignKey(Account_Due, verbose_name='应收款', on_delete=models.CASCADE)
    cancel = models.FloatField(verbose_name='本次核销', default=0)

    class Meta:
        verbose_name = '应收款核销记录'
        verbose_name_plural = verbose_name
