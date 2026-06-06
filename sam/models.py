from django.db import models
import random

class Customer(models.Model):

    username = models.CharField(max_length=100)

    email = models.EmailField(max_length=100)

    password = models.CharField(max_length=255)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

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