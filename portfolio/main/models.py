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
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    portfolio = models.ManyToManyField(Stock, blank=True, null=True)
    def __str__(self):
        return f'{self.name} - {self.email})'






