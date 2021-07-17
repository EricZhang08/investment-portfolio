from django.contrib import admin
from .models import Stock, User, Ticker

# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'id')
  list_filter = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Stock)
admin.site.register(Ticker)
