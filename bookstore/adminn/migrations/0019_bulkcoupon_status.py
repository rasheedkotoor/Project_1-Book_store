# Generated by Django 3.1.7 on 2021-04-09 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminn', '0018_bulkcoupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkcoupon',
            name='status',
            field=models.CharField(default='active', max_length=10),
        ),
    ]
