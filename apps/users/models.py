from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=12, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    number = models.CharField(verbose_name='工号', max_length=120, default='', blank=True)
    login_times = models.PositiveIntegerField(verbose_name='登录次数', blank=True, default=0)
    department = models.CharField(verbose_name='部门', max_length=120, blank=True, null=True)
    role = models.CharField(verbose_name='角色', max_length=120, blank=True, null=True)
    remarks = models.CharField(verbose_name='备注', max_length=120, blank=True, null=True)
    operate = models.CharField(verbose_name='操作', max_length=120, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
