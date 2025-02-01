from django.db import models
from autoslug import AutoSlugField
from decimal import Decimal
from django.contrib.auth.models import User
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
        ('percentage', '%'),# % is the percentage symbol
        ('fixed', '₹'),#₹ is the Indian Rupee symbol
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name', unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    gender_age_group = models.CharField(max_length=1, choices=[('M', 'Man'), ('W', 'Woman'), ('B', 'Boy'), ('G', 'Girl'), ('A', 'All')],default='A')
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        original_price = self.original_price
        discount_value = self.discount_value
        discount_type = self.discount_type

        if discount_value is not None:
            if discount_type == 'percentage':
                return round(original_price * (1 - discount_value / 100),2)
            elif discount_type == 'fixed':
                return round(original_price - discount_value,2)

def __str__(self):
    return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image of {self.product.name}"
    
