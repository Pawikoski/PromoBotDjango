# Generated by Django 4.0.4 on 2022-05-15 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=60)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('wanted_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('wanted_price_tolerance', models.IntegerField()),
                ('wanted_price_notifications', models.JSONField()),
                ('lowest_price_notification_time_value', models.IntegerField()),
                ('lowest_price_notification_time_unit', models.CharField(choices=[('m', 'Minutes'), ('h', 'Hours')], max_length=1)),
                ('lowest_price_notifications', models.JSONField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='priceBot.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('tags', models.CharField(max_length=300)),
                ('url', models.URLField(unique=True)),
                ('photo_url', models.URLField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ProductUrls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urls', models.JSONField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='priceBot.product')),
            ],
        ),
    ]
