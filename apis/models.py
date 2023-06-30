from django.db import models
import random
import re
from PIL import Image
from io import BytesIO
from django.core.files import File


class Products(models.Model):
    itemName = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.CharField(max_length=255)  # Specify the max_length for the quantity field
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.itemName

def upload_location(instance, filename):
    ext = filename.split(".")[-1]
    shop = re.sub(r'\W+', '', instance.shop.shopname)
    item_name = re.sub(r'\W+', '', instance.title)
    category = re.sub(r'\W+', '', instance.category)
    num = random.randint(1000, 9999)

    filename = "{}.{}.{}".format(item_name, category, num)

    return "{}/{}.{}".format(shop, filename, ext)

class Shop(models.Model):
    shopname = models.CharField(max_length=255, default='null')
    location = models.CharField(max_length=255, default='null')

    def __str__(self):
        return f'Shop {self.id}: {self.shopname}: {self.location}'


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, default='null')
    price=models.DecimalField(max_digits=20, decimal_places=2, null=True)
    
    category = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        if self.shop:
            self.location = self.shop.location  # Assign the location from the associated shop
       
            

            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    