# Generated by Django 4.1.13 on 2024-06-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_subscription_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='field_a',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='subscription',
            name='field_b',
            field=models.CharField(default='', max_length=50),
        ),
    ]
