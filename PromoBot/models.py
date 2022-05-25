from django.db import models

# Create your models here
class Store(models.Model):
    name = models.CharField(max_length=60)
    url = models.URLField(max_length=128, blank=True)
    
    def __str__(self):
        return self.name


class StoreCategory(models.Model):
    name = models.CharField(max_length=60)
    available_stores = models.ManyToManyField(Store)
    
    class Meta:
        verbose_name = "Store category"
        verbose_name_plural = "Stores categories"
        
    def __str__(self):
        return self.name
    

class StoreCategoryURL(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)
    url = models.URLField(max_length=255, blank=True)
    
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
    url = models.URLField(max_length=256)
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
    