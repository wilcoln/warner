# Generated by Django 2.2.4 on 2019-08-22 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
