# Generated by Django 4.0.4 on 2022-12-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_order_order_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Battery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('but', models.CharField(db_index=True, max_length=100, verbose_name='Батарея')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
            ],
        ),
    ]
