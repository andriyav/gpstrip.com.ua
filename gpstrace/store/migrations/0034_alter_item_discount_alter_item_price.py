# Generated by Django 4.0.4 on 2022-11-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_item_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True, verbose_name='Знижка у %'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True, verbose_name='Ціна товару'),
        ),
    ]
