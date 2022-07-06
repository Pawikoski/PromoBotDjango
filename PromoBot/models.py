from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here
class Store(models.Model):
    name = models.CharField(max_length=60)
    url = models.URLField(max_length=128, blank=True)
    
    def __str__(self):
        return self.name


class StoreCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    available_stores = models.ManyToManyField(Store, blank=True)
    
    class Meta:
        verbose_name = "Store category"
        verbose_name_plural = "Stores categories"
        
    def __str__(self):
        return self.name
    

class StoreCategoryURL(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)
    url = models.URLField(max_length=255, blank=True)
    
    class Meta:
        unique_together = ["store", "category"]
    
    def __str__(self):
        return f"{self.category} - {self.store}"
    

# class ProductCategory(models.Model):
#     name = models.CharField(max_length=60)
    
#     class Meta:
#         verbose_name = "Product category"
#         verbose_name_plural = "Products categories"
        
#     def __str__(self):
#         return "Promobot Product Category - " + self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(StoreCategory, on_delete=models.SET_NULL, null=True)
    url = models.URLField(max_length=256, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    best_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    best_price_date = models.DateField(null=True)
    available = models.BooleanField(default=True)
    
    
    class Meta:
        verbose_name = "Product"    
        verbose_name_plural = "Products"    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.last_price and not self.best_price:
            self.last_price = self.price
            self.best_price = self.price
            self.best_price_date = datetime.date.today().strftime("%Y-%m-%d")
            
        super(Product, self).save(*args, **kwargs)
    

class Thumbnail(models.Model):
    product = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE)
    img_url = models.URLField(max_length=512, null=True)
    

class Promo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    certain = models.BooleanField(default=True)
    liked = models.ManyToManyField(User, default=None, blank=True)
    
    @property
    def num_likes(self):
        return self.liked.all().count()
    

class PromoComment(models.Model):
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike')
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)
    
    def __str__(self):
        return str(self.promo)