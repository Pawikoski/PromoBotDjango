# Generated by Django 4.0.4 on 2022-05-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('priceBot', '0002_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='promobot_api_key',
            field=models.UUIDField(blank=True, unique=True),
        ),
    ]
