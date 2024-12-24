from django.contrib.auth.backends import BaseBackend
from seller.models import Seller

class SellerBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            seller = Seller.objects.get(username=username)
            if seller.check_password(password):
                # Attach the backend attribute
                seller.backend = 'seller.backends.SellerBackend'
                return seller
        except Seller.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Seller.objects.get(pk=user_id)
        except Seller.DoesNotExist:
            return None
