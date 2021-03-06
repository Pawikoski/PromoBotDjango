# Generated by Django 4.0.4 on 2022-05-22 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PromoBot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='category',
        ),
        migrations.AddField(
            model_name='storecategory',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PromoBot.store'),
        ),
        migrations.AddField(
            model_name='storecategory',
            name='url',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='PromoBot.storecategory'),
        ),
        migrations.AlterField(
            model_name='store',
            name='url',
            field=models.URLField(blank=True, max_length=128),
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]
