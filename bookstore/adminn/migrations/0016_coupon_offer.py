# Generated by Django 3.1.7 on 2021-04-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminn', '0015_auto_20210404_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='offer',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
