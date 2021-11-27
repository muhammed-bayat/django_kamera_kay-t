from django.contrib import admin

# Register your models here.
from opencvdjango.models import UserEntry


class UserEntryAdmin(admin.ModelAdmin):
    list_display = (  'header', 'description', 'created_date', 'rating')

admin.site.register(UserEntry, UserEntryAdmin)