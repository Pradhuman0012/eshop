from django.db import models

# Create your models here.


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Home Goods', 'Home Goods'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/',null=True, blank=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    