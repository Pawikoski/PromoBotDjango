# Generated by Django 4.0.5 on 2022-06-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PromoBot', '0009_promo_liked_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storecategory',
            name='available_stores',
            field=models.ManyToManyField(blank=True, to='PromoBot.store'),
        ),
    ]
