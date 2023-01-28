# Generated by Django 4.0.4 on 2022-12-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_battery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='battery',
            field=models.IntegerField(blank=True, choices=[(1000, 1000), (5000, 5000), (10000, 10000), (20000, 20000)], max_length=20, null=True, verbose_name='Ємність акумуляторної батареї'),
        ),
    ]