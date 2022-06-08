# Generated by Django 4.0.5 on 2022-06-07 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PromoBot', '0008_promo_certain'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')], default='Like', max_length=10)),
                ('promo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PromoBot.promo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]