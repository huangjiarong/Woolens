# Generated by Django 2.0 on 2019-04-21 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190421_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='number',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='工号'),
        ),
    ]
