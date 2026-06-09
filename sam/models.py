from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class Customer(AbstractUser):

    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class OTP(models.Model):

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def generate_otp(self):

        code = str(random.randint(100000,999999))

        self.otp = code

        self.save()

        return code
    


class Product(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.IntegerField()

    image = models.ImageField(
        upload_to='products/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    
class Cart(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

class Wishlist(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

class RecentSearch(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    keyword = models.CharField(
        max_length=200
    )

    searched_at = models.DateTimeField(
        auto_now_add=True
    )