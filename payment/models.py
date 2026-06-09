from django.db import models
from sam.models import * 

class Order(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    order_number = models.CharField(
        max_length=50,
        unique=True
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        default='pending'
    )

    status = models.CharField(
        max_length=20,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

class Payment(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    razorpay_order_id = models.CharField(
        max_length=255
    )

    razorpay_payment_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        default="created"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )