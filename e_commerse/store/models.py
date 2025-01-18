from django.db import models
from autoslug import AutoSlugField
from decimal import Decimal
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
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # price field
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name', unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    gender_age_group = models.CharField(max_length=1, choices=[('M', 'Man'), ('W', 'Woman'), ('B', 'Boy'), ('G', 'Girl'), ('A', 'All')],default='A')
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
            # Set the price to be the same as original_price if it's not already set
            if self.discount_value is None:
                self.price = self.original_price
            else:
                # Recalculate the discounted price based on the type of discount
                if self.discount_type == 'percentage':
                    # Ensure both operands are Decimals
                    self.price = Decimal(self.original_price) * (1 - Decimal(self.discount_value) / Decimal(100))
                elif self.discount_type == 'fixed':
                    self.price = Decimal(self.original_price) - Decimal(self.discount_value)
            
            super(Product, self).save(*args, **kwargs)

def __str__(self):
    return self.name
# def get_discounted_price(self):
#     """Calculate the final price after discount."""
#     if self.discount_value:
#         # Ensure the discount_value and original_price are Decimal
#         original_price = Decimal(self.original_price)
#         discount_value = Decimal(self.discount_value)
        
#         if self.discount_type == 'percentage':
#             return original_price * (1 - discount_value / 100)
#         elif self.discount_type == 'fixed':
#             return original_price - discount_value
#     return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image of {self.product.name}"