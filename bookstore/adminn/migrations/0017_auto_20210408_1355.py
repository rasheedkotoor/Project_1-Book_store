# Generated by Django 3.1.7 on 2021-04-08 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20210404_1252'),
        ('adminn', '0016_coupon_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
    ]
