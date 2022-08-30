
from django.db import models

# Create your models here.
class Categories(models.Model):
    category_name = models.CharField(max_length=42)
    category_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


#таблица продуктов
class Products(models.Model):
    product_name = models.CharField(max_length=42)
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_price = models.FloatField()
    product_description = models.TextField()
    product_count = models.IntegerField()
    product_date = models.DateTimeField(auto_now_add=True)
    product_image = models.ImageField(upload_to='media', blank=True, null=True)

    def __str__(self):
        return self.product_name

#Таблица корзины
class UserCart(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)