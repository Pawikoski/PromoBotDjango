import base64
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import json

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=60)
    
    
class StoreCategory(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Store Category"
        verbose_name_plural = "Stores Categories"
    
    
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


class Store(models.Model):
    name = models.CharField(max_length=40)
    category = models.ManyToManyField(StoreCategory)
    tags = models.CharField(max_length=300)
    url = models.URLField(unique=True)
    photo_url = models.URLField(max_length=300)
    is_premium = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"
    
    def __str__(self):
        return self.name
    

class ProductUrls(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    urls = models.JSONField()
    
    def save(self, *args, **kwargs):
        if not self.urls:
            self.urls = json.dumps({"urls": []})
            super(ProductUrls, self).save(*args, **kwargs)
        else:
            super(ProductUrls, self).save(*args, **kwargs)


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    promobot_api_key = models.UUIDField(max_length=128, blank=True, unique=True, null=True)
    token = models.BinaryField(blank=True)
    telegram_api_key = models.CharField(max_length=128, blank=True, null=True)
    telegram_user_id = models.IntegerField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.token = base64.b64encode(str(self.promobot_api_key).encode('ascii'))
        super(UserData, self).save(*args, **kwargs)
        

# class UserSettings(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     premium = models.BooleanField(default=False)
#     premium_end = models.DateTimeField(blank=True)
#     time_break_between_requests_value = models.IntegerField()
#     TIME_UNIT_CHOICES = (
#         ("m", "Minutes"),
#         ("h", "Hours")
#     )
#     time_break_between_requests_unit = models.CharField(choices=TIME_UNIT_CHOICES, max_length=1)
    

class ProductStat(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    lowest_price = models.DecimalField(max_digits=8, decimal_places=2)
    lowest_price_date = models.DateTimeField(auto_now=True)
    lowest_price_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="lowest_price_so_far_store")
    last_check_date = models.DateTimeField(auto_now=True)
    last_check_lowest_price = models.DecimalField(max_digits=8, decimal_places=2)
    last_check_lowest_price_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="lowest_price_last_check_store")

    
class Version(models.Model):
    version = models.CharField(max_length=50)
    

class Download(models.Model):
    windows_version = models.FileField(upload_to='releases/')
    linux_version = models.FileField(upload_to='releases/')
    mac_version = models.FileField(upload_to='releases/')
