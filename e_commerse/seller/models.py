from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)  # Auto-increment primary key field
    owner_name = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    shop_address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=150, unique=True)  # Username for login
    password = models.CharField(max_length=128)  # Store hashed passwords
    last_login = models.DateTimeField(blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    @property
    def is_authenticated(self):
        # Always return True for authenticated users
        return True

    def __str__(self):
        return f"{self.shop_name} - {self.owner_name}"
