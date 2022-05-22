# Generated by Django 4.0.4 on 2022-05-22 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('priceBot', '0013_store_is_premium'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Store Category',
                'verbose_name_plural': 'Stores Categories',
            },
        ),
        migrations.AlterModelOptions(
            name='store',
            options={'verbose_name': 'Store', 'verbose_name_plural': 'Stores'},
        ),
    ]
