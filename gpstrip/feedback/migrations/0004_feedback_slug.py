# Generated by Django 4.0.4 on 2023-02-11 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_feedback_time_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='slug',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
