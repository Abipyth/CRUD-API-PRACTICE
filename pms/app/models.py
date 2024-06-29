from django.db import models
from django.contrib.auth.models import User
import binascii
import os

class Product(models.Model):
    name=models.CharField(max_length=25)
    desc=models.TextField()

    def __str__(self):
        return self.name

class APIkey(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    key=models.CharField(max_length=40, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key=self.generate_key()
        return super().save(*args, **kwargs)
    
    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    def __str__(self):
        return f'{self.user.username}-{self.key}'