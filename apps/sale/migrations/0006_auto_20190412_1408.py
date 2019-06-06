# Generated by Django 2.0 on 2019-04-12 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0005_auto_20190412_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleexport',
            name='sale_order',
        ),
        migrations.AddField(
            model_name='saleexport',
            name='sale_order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sale.SaleOrder', verbose_name='所属销售订单'),
            preserve_default=False,
        ),
    ]
