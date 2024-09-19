from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)  # Product name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    image = models.ImageField(upload_to='product_images/')  # Image upload path
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})  # Only superusers can add
    date_added = models.DateTimeField(auto_now_add=True)  # When the product was added

    def __str__(self):
        return self.name
