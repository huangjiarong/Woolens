# Generated by Django 2.0 on 2019-04-02 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancillaryData', '0002_auto_20190402_1116'),
        ('baseData', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='type',
        ),
        migrations.AddField(
            model_name='client',
            name='type',
            field=models.ManyToManyField(to='ancillaryData.ClientType', verbose_name='客户类别'),
        ),
    ]
