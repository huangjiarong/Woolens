# Generated by Django 2.0 on 2019-04-23 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money_management', '0010_auto_20190419_2151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account_due',
            options={'permissions': (('view_account_due', '查看应收款'),), 'verbose_name': '应收款', 'verbose_name_plural': '应收款'},
        ),
        migrations.AlterModelOptions(
            name='receipt',
            options={'permissions': (('view_receipt', '查看收款单'),), 'verbose_name': '付款单', 'verbose_name_plural': '付款单'},
        ),
        migrations.AlterField(
            model_name='account_due',
            name='business_type',
            field=models.CharField(choices=[('订货', '订货'), ('购货', '购货'), ('销货出货应收款', '销货出货应收款'), ('销货应收款', '销货应收款'), ('摇纱', '摇纱'), ('拼纱', '拼纱'), ('染色', '染色'), ('打毛', '打毛')], max_length=60, verbose_name='业务类别'),
        ),
        migrations.AlterField(
            model_name='due',
            name='business_type',
            field=models.CharField(choices=[('订货', '订货'), ('购货', '购货'), ('销货出货应收款', '销货出货应收款'), ('销货应收款', '销货应收款'), ('摇纱', '摇纱'), ('拼纱', '拼纱'), ('染色', '染色'), ('打毛', '打毛')], max_length=60, verbose_name='业务类别'),
        ),
    ]
