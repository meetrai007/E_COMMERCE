from django.db import models
from autoslug import AutoSlugField
from seller.models import Seller

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name', unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    gender = models.CharField(max_length=1, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both'),
    ])
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        """Calculate the final price after discount."""
        if self.discount_value:
            if self.discount_type == 'percentage':
                return self.original_price * (1 - self.discount_value / 100)
            elif self.discount_type == 'fixed':
                return self.original_price - self.discount_value
        return self.price

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image of {self.product.name}"