# Generated by Django 4.0.4 on 2022-12-29 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_item_battery'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
