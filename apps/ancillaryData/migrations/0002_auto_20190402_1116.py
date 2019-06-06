# Generated by Django 2.0 on 2019-04-02 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ancillaryData', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clienttype',
            name='pre_type',
        ),
        migrations.AlterUniqueTogether(
            name='clienttype',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='packaging',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='warehousetype',
            unique_together={('name',)},
        ),
        migrations.RemoveField(
            model_name='woolenstype',
            name='pre_type',
        ),
        migrations.AlterUniqueTogether(
            name='woolenstype',
            unique_together={('name',)},
        ),
    ]