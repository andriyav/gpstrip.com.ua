# Generated by Django 4.0.4 on 2022-12-21 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_order_address_np_order_first_name_np_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_notes',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]