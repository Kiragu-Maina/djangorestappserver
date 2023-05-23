from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.db import models

class AbstractProducts(models.Model):
    itemName = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')

    # Add any additional fields or methods as needed

    def __str__(self):
        return self.itemName

class CustomProduct(AbstractProduct):
    # Link the custom product class to your AbstractProducts model
    abstractproduct_ptr = models.OneToOneField(
        AbstractProduct, on_delete=models.CASCADE, parent_link=True, related_name='custom_product'
    )
    # Add any additional fields or methods specific to your custom product class

    class Meta:
        app_label = 'apis'
        verbose_name = 'Product'

    def get_absolute_url(self):
        # Customize the product detail URL as needed
        return f'/products/{self.slug}/'
