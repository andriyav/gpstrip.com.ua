# Generated by Django 4.0.4 on 2022-10-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_item_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='details',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Деталі'),
        ),
    ]