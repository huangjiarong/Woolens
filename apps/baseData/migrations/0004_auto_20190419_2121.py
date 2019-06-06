# Generated by Django 2.0 on 2019-04-19 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseData', '0003_auto_20190411_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='pre_receivable',
            field=models.FloatField(blank=True, default=0, verbose_name='期初预收款'),
        ),
        migrations.AlterField(
            model_name='client',
            name='receivable',
            field=models.FloatField(blank=True, default=0, verbose_name='期初应收款'),
        ),
    ]