# Generated by Django 4.0.4 on 2022-05-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('priceBot', '0006_alter_producturls_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='promobot_api_key',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
