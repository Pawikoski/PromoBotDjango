# Generated by Django 4.0.5 on 2022-06-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PromoBot', '0010_alter_storecategory_available_stores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='img_url',
            field=models.URLField(max_length=512, null=True),
        ),
    ]