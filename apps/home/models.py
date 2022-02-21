# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime

from django.db import models
from django.db.models import Count, Sum, Q
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

at_least_zero = MinValueValidator(0, 'Der Wert muss höher als null sein.')


class Drink(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(validators=[at_least_zero])
    amount = models.IntegerField(validators=[at_least_zero])

    def __str__(self):
        return self.name


class Bbr(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30,
                              choices=[('FUX', 'Fux'), ('BURSCH', 'Bursch'), ('AH', 'Alter Herr'), ('', '')],
                              null=True)
    # Eine der Optionen: Fux, Bursch, Alter Herr
    position = models.CharField(max_length=30, null=True)  # Amt des Bbrs

    def get_marks(self, start=(datetime.datetime.now() - datetime.timedelta(days=30)), end=datetime.datetime.now()):
        q1 = self.mark_set.filter(timestamp__gte=start, timestamp__lte=end)
        q2 = q1.aggregate(bier=Sum('units', filter=Q(drink=1)),
                          kasten=Sum('units', filter=Q(drink=2)),
                          wein=Sum('units', filter=Q(drink=3)))
        price = 0
        for mark in self.mark_set.all():
            price += mark.get_price
        q2['preis'] = price
        q2['full_name'] = self.user.get_full_name()
        return q2

    def __str__(self):
        return self.user.username


class Mark(models.Model):
    bbr = models.ForeignKey(Bbr, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True)
    units = models.IntegerField(validators=[at_least_zero], null=True)

    @property
    def get_price(self):
        price = self.drink.price * self.units
        return price

    def sum_marks(self, bbr, start, end):
        self.objects.filter()



