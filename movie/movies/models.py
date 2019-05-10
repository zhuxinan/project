from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class MyUser(User):
    uicon = models.ImageField(upload_to='%Y/%m/%d/icons',null=True,blank=True)

class Movies(models.Model):
    title = models.CharField(max_length=50,unique=True)
    image = models.CharField(max_length=200)
    duration = models.IntegerField(default=0)
    class Meta():
        verbose_name = '电影'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class Collections(models.Model):
    mid = models.ForeignKey(Movies,on_delete=models.CASCADE,null=True,unique=True)
    uid = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    class Meta():
        verbose_name = '收藏'
        verbose_name_plural = verbose_name