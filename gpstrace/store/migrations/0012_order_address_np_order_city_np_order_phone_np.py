# Generated by Django 4.0.4 on 2022-12-19 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_order_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address_np',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='city_np',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_np',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
