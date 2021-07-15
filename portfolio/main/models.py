from django.db import models
from django import forms

# Create your models here.

class Stock(models.Model):
    ticker = models.CharField(max_length=30)
    percentage = models.FloatField()

    def __str__(self):
        return self.ticker

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    portfolio = models.ManyToManyField(Stock)
    def __str__(self):
        return f'{self.name} - {self.email})'





