from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cateogry = models.CharField(max_length=60)
    
    
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=60)
    
    wanted_price = models.DecimalField(max_digits=8, decimal_places=2)
    wanted_price_tolerance = models.IntegerField()
    wanted_price_notifications = models.JSONField()
    
    TIME_UNIT_CHOICES = (
        ("m", "Minutes"),
        ("h", "Hours")
    )
    lowest_price_notification_time_value = models.IntegerField()
    lowest_price_notification_time_unit = models.CharField(max_length=1, choices=TIME_UNIT_CHOICES)
    lowest_price_notifications = models.JSONField()


class ProductUrls(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    urls = models.JSONField()