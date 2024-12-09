from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)  # Auto-increment primary key field
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    owner_name = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    shop_address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.shop_name} - {self.owner_name}"