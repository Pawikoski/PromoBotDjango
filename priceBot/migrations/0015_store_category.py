# Generated by Django 4.0.4 on 2022-05-22 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('priceBot', '0014_storecategory_alter_store_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='priceBot.storecategory'),
        ),
    ]
