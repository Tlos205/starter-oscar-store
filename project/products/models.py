from django.db import models
from oscar.apps.catalogue.models import Product

class DigitalProduct(models.Model):
    """Простая модель цифрового товара"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to='digital/')
    
    def __str__(self):
        return f"Цифровая версия: {self.product.title}"