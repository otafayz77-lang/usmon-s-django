from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    


class Product(models.Model):
    Nomi = models.CharField(max_length=100)
    Narxi = models.IntegerField()
    Malumoti = models.TextField()
    Rasmi = models.ImageField(upload_to='odam/')
    Yili = models.DateField()
    Holati = models.CharField(max_length=100)
    Kategoriya = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Nomi


class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_product')
        ]

    @property
    def total_price(self):
        return self.product.Narxi * self.count

    def __str__(self):
        return self.product.Nomi
    

class Transaction(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.product.Nomi