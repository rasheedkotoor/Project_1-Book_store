import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    code = models.CharField(max_length=15, null=True, blank=True, unique=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='ref_by')
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, null=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommended_profiles(self):
        qs = Profile.objects.all()
        my_recs = [p for p in qs if p.recommended_by == self.user]
        return my_recs

    @property
    def imageurl11(self):
        if self.image == '':
            image = ' '
        else:
            image = self.image.url
        return image


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)


