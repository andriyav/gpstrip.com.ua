# Generated by Django 4.0.4 on 2023-02-22 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_delete_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
