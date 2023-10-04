from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class PasswordReset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.IntegerField(default=0)
    valid_til = models.DateTimeField()
    password_updated = models.BooleanField(default=False)
    token = models.CharField(max_length=250)


    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username