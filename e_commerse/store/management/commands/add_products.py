from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Product, Category
from seller.models import Seller
from store.models import ProductImage
import os

class Command(BaseCommand):
    help = 'Add 50 products to the database with multiple images'

    def handle(self, *args, **kwargs):
        category = Category.objects.first()
        seller = Seller.objects.first()

        if not category or not seller:
            self.stdout.write("Ensure you have at least one Category and Seller in the database.")
            return

        photo_path = 'media/products/8-rmx3085-realme-original-imagfgpgcx2cp89f_5ZBLo3y.webp'

        if not os.path.exists(photo_path):
            self.stdout.write(f"Photo file not found at {photo_path}. Ensure the path is correct.")
            return

        for i in range(1, 51):
            product_name = f"Product {i}"
            product = Product(
                name=product_name,
                category=category,
                seller=seller,
                price=9.99,
                quantity=10,
                description="""About this item
Monster Durability & Display : Corning Gorilla Glass Victus+, 16.83 Centimeters (6.6Inch) Super AMOLED Display, FHD+ Resolution with 1080 x 2340 Pixels and 120Hz Refresh Rate
Monster Processor - Exynos 1380 Processor with Vapour Cooling Chamber | Latest Android 14 Operating System having One UI 6.1 platform | 2.4GHz, 2GHz Clock Speed with Octa-Core Processor
Monster Convenience & Security - Samsung Wallet with Tap & Pay | Knox Security | Get upto 4 Generations of AndroidOS Upgrades & 5 Years of Security Updates
Monster Camera - 50MP (F1.8) Main Wide Angle Camera + 8MP (F2.2) Ultra Wide Angle Camera + 2MP (F2.4) Macro Angle Camera | OIS & Nightography | 13MP (F2.2) Selfie Camera | Video Maximum Resolution of Ultra HD (3840 x 2160) @30fps
Monster Battery - Get a massive 6000mAh Lithium-ion Battery (Non-Removable) with C-Type Fast Charging (25W Charging Support),"""
            )

            product.save()  # Save the product first to generate an ID

            # Save the main product photo 5 times
            for _ in range(5):
                with open(photo_path, 'rb') as photo_file:
                    product_image = ProductImage(
                        product=product
                    )
                    product_image.image.save(f"{product_name}_image.jpg", File(photo_file), save=False)
                    product_image.save()

            self.stdout.write(f"Added {product_name} with 5 images.")
