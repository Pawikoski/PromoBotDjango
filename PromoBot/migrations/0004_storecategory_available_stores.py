# Generated by Django 4.0.4 on 2022-05-24 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PromoBot', '0003_remove_storecategory_store_remove_storecategory_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storecategory',
            name='available_stores',
            field=models.ManyToManyField(to='PromoBot.store'),
        ),
    ]
