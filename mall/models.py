from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Stuff(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    detail = RichTextUploadingField('내용', blank=True, null=True)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="", blank=True)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stuffs = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' ' + self.stuffs.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order_date = models.DateTimeField()
    subtotal = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' ' + self.stuff.name+' '+str(self.order_date)


class Month(models.Model):
    month = models.CharField(max_length=200, blank=True, null=True)


class Day(models.Model):
    day = models.CharField(max_length=200, blank=True, null=True)
    remain_seat = models.IntegerField(blank=True, null=True)
    f_month = models.ForeignKey(
        Month, on_delete=models.CASCADE, blank=True, null=True)


def image_upload_path(instance, filename):
    return f'{instance.stuff.id}/{filename}'


class PostImage(models.Model):
    stuff = models.ForeignKey(
        Stuff, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to=image_upload_path,
                               blank=True, null=True)
    add_date = models.DateTimeField()

    def __str__(self):
        return self.stuff.name + '-' + str(self.add_date)
