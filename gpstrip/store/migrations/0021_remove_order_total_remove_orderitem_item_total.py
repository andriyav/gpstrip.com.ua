# Generated by Django 4.0.4 on 2022-12-29 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_orderitem_item_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='item_total',
        ),
    ]