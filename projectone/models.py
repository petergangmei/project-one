from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# from account.models import *
import random

class Company(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True,blank=True,null=True)
    about = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        try:
            Company.objects.get(slug=slugify(self.name))
            self.slug = slugify(self.name)+"-"+str(random.randint(11111,99999))
        except Company.DoesNotExist:
            self.slug = slugify(self.name)
        super(Company,self).save(*args,**kwargs)
    