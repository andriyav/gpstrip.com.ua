# Generated by Django 4.0.4 on 2022-06-13 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_item_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('Новика', 'Новинка'), ('Популярне', 'Популярне')], max_length=20, null=True, verbose_name='Акційна мітка'),
        ),
    ]
