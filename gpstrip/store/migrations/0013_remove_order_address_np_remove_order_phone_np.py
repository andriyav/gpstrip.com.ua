# Generated by Django 4.0.4 on 2022-12-20 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_order_address_np_order_city_np_order_phone_np'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address_np',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone_np',
        ),
    ]