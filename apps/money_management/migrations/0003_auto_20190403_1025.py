# Generated by Django 2.0 on 2019-04-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money_management', '0002_auto_20190403_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='due',
            name='ord_num',
            field=models.CharField(max_length=60, null=True, verbose_name='单号'),
        ),
    ]
