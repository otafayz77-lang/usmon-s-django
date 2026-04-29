from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User_profile(models.Model):
    name = models.CharField(max_length=100)
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


class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_product')
 
        ]



    def __str__(self):
        return self.Nomi
    

class Transaction(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User_profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.product.Nomi