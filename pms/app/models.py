from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    name=models.CharField(max_length=25)
    desc=models.TextField()

    def __str__(self):
        return self.name

