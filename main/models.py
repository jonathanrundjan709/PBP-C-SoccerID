from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("", "Pilih Kategori"),
        ("jersey", "Jersey"),
        ("sepatu", "Sepatu"),
        ("aksesoris", "Aksesoris"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    price = models.CharField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])  # stok produk
    is_featured = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"

    @property
    def is_in_stock(self):
        return self.stock > 0
    
