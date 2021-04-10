from django.db import models
import datetime, uuid
from django.shortcuts import reverse
from django.conf import settings
from user.models import Address, Profile


# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=150)
    offer = models.IntegerField(default=0)


class Author(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    email = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='prfl/', height_field=None, width_field=None, null=True)


class Books(models.Model):
    YEAR_CHOICES = [(r, r) for r in range(1900, datetime.date.today().year + 1)]
    CURRENT_YEAR = datetime.date.today().year

    name = models.CharField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.CharField(max_length=100)
    year = models.IntegerField('year', choices=YEAR_CHOICES, default=CURRENT_YEAR)
    edition = models.CharField(max_length=100)
    page_no = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    offer = models.FloatField()
    description = models.TextField()
    image1 = models.ImageField(upload_to='images/', height_field=None, width_field=None, null=True)
    image2 = models.ImageField(upload_to='images/', height_field=None, width_field=None, null=True)
    image3 = models.ImageField(upload_to='images/', height_field=None, width_field=None, null=True)


    @property
    def disc_price(self):
        real_price = self.price * self.offer / 100
        di_price = self.price - real_price
        return di_price

    @property
    def imageurl1(self):
        if self.image1 == '':
            image = ' '
        else:
            image = self.image1.url
        return image

    @property
    def imageurl2(self):
        if self.image2 == '':
            image = ' '
        else:
            image = self.image2.url
        return image

    @property
    def imageurl3(self):
        if self.image3 == '':
            image = ' '
        else:
            image = self.image3.url
        return image


class Cart(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Ordered', 'Ordered'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')
    date = models.DateField(auto_now=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.book.name}"


class Order(models.Model):
    STATUS = (
        ('Placed', 'Placed'),
        ('Canceled', 'Canceled'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
    )
    PAY_STATUS = (
        ('SUCCESS', 'SUCCESS'),
        ('FAILURE', 'FAILURE'),
        ('PENDING', 'PENDING'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    price = models.FloatField()
    offer = models.FloatField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=50, default='Placed')
    pay_status = models.CharField(choices=PAY_STATUS, max_length=10, default='SUCCESS')
    pay_method = models.CharField(max_length=50)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)
    coupon_code = models.CharField(max_length=15)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, default='active')
    date = models.DateField(auto_now=True)


class BulkCoupon(models.Model):
    name = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, default='active')
