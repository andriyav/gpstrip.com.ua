# Generated by Django 4.0.4 on 2023-02-13 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_feedback_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='rate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]