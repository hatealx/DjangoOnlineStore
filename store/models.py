from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Unique name for the category
    description = models.TextField(blank=True)  # Optional description for the category

    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=200)  # Product name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    image = models.ImageField(upload_to='product_images/')  # Image upload path
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})  # Only superusers can add
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Product category
    date_added = models.DateTimeField(auto_now_add=True)  # When the product was added
    stock = models.PositiveIntegerField(default=0)  # Product stock
    featured = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        
        return self.name





class Command(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    details = models.TextField()  # User will write everything here (quantity, address, etc.)
    created_at = models.DateTimeField(auto_now_add=True)  # To store when the command was made

    def __str__(self):
        return f'Command {self.id} by {self.user.username} for {self.product.name}'
    