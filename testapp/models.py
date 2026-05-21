from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    stock = models.IntegerField()

    image = models.ImageField(
        upload_to='products/'
    )

    rating = models.FloatField(
        default=4.5
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    def __str__(self):
        return self.name


class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    def __str__(self):
        return self.product.name


class Order(models.Model):

    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Shipped', 'Shipped'),

        ('Delivered', 'Delivered'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    def __str__(self):
        return self.product.name