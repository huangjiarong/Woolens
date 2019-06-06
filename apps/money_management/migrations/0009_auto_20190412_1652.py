# Generated by Django 2.0 on 2019-04-12 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money_management', '0008_auto_20190411_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_to_Due',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel', models.FloatField(default=0, verbose_name='本次核销')),
                ('due', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_management.Due', verbose_name='应付款')),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='due',
        ),
        migrations.AddField(
            model_name='payment_to_due',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_management.Payment', verbose_name='付款单'),
        ),
        migrations.AddField(
            model_name='payment',
            name='due',
            field=models.ManyToManyField(through='money_management.Payment_to_Due', to='money_management.Due', verbose_name='对应应付款单'),
        ),
    ]
