from django.db import models
from seller.models import Seller
from autoslug import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # Field to store category photo

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products', null=True, blank=True)  # Link to Seller
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name', unique=True)
    # Removing single photo field, as we will now use ProductImage to store multiple images
    # photo = models.ImageField(upload_to='products/', blank=True, null=True) 

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)  # Link each image to a product
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Field to store product image

    def __str__(self):
        return f"Image for {self.product.name}"
