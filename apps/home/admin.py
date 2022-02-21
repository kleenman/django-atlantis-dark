# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Drink, Bbr, Mark
# Register your models here.


class DrinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'amount')


class BbrAdmin(admin.ModelAdmin):
    pass


class MarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'bbr', 'drink', 'units', 'timestamp')
    list_filter = ('bbr', 'drink')


admin.site.register(Drink, DrinkAdmin)
admin.site.register(Bbr, BbrAdmin)
admin.site.register(Mark, MarkAdmin)
