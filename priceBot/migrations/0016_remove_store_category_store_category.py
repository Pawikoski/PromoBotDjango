# Generated by Django 4.0.4 on 2022-05-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('priceBot', '0015_store_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='category',
        ),
        migrations.AddField(
            model_name='store',
            name='category',
            field=models.ManyToManyField(null=True, to='priceBot.storecategory'),
        ),
    ]
