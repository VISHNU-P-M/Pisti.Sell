from django.db import models

# Create your models here.
class Categories(models.Model):
    category = models.CharField(max_length=30)
    
class Brands(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)