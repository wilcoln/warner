# Generated by Django 2.2.4 on 2019-09-05 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warner', '0007_auto_20190904_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='epoch',
            new_name='episode',
        ),
        migrations.AlterModelTable(
            name='episode',
            table='episode',
        ),
    ]
