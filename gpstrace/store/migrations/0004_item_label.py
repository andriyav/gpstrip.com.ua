# Generated by Django 4.0.4 on 2022-05-21 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_discount_price_item_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('N', 'Новинка'), ('P', 'Популярне')], max_length=1, null=True),
        ),
    ]