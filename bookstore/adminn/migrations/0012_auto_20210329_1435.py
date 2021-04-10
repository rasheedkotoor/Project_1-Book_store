# Generated by Django 3.1.7 on 2021-03-29 09:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminn', '0011_auto_20210327_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered_date',
        ),
        migrations.AddField(
            model_name='order',
            name='start_time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]