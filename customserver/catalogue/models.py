
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractAttributeOptionGroup, AbstractAttributeOption, AbstractProductCategory, AbstractOption, AbstractProductAttributeValue, AbstractProductRecommendation, AbstractProductClass, AbstractProductImage, AbstractProductAttribute, AbstractCategory, AbstractProductClass
from django.db import models
from django.utils import timezone


class Option(AbstractOption):
    pass

class ProductAttribute(AbstractProductAttribute):
    pass

class ProductAttributeValue(AbstractProductAttributeValue):
    pass

class ProductCategory(AbstractProductCategory):
    pass

class ProductClass(AbstractProductClass):
    pass

class ProductImage(AbstractProductImage):
    pass

class ProductRecommendation(AbstractProductRecommendation):
    pass


class AttributeOption(AbstractAttributeOption):
    pass


class AttributeOptionGroup(AbstractAttributeOptionGroup):
    pass

class Category(AbstractCategory):
    pass

def default_description():
        return f'created at:{timezone.now}'

class Product(AbstractProduct):
    itemName = models.CharField(max_length=255, default=default_description())
    descriptionfieldy = models.TextField(default=default_description())
    pricefieldy = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    quantityfieldy = models.PositiveIntegerField(default=0)
    imagefieldy = models.ImageField(upload_to='product_images/', default='product_images/default_image.jpg')


    

    def __str__(self):
        return self.itemName


    
