from django.contrib import admin
from .models import Stock, User

# Register your models here.

class MeetupAdmin(admin.ModelAdmin):
  list_display = ('name', 'email')
  list_filter = ('name',)

admin.site.register(User, MeetupAdmin)
admin.site.register(Stock)
