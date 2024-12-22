from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Check if the OTP is valid (within 5 minutes of creation)
        return now() <= self.created_at + timedelta(minutes=5)
