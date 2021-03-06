# Generated by Django 4.0.4 on 2022-05-30 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PromoBot', '0005_product_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='PromoBot.product')),
                ('img_url', models.URLField(max_length=256, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='storecategoryurl',
            unique_together={('store', 'category')},
        ),
    ]
