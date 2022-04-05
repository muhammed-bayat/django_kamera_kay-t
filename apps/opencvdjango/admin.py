from django.contrib import admin

# Register your models here.
from .models import UserEntry, UserAnswer


class UserEntryAdmin(admin.ModelAdmin):
    list_display = ('header', 'description', 'created_date', 'rating')

admin.site.register(UserEntry, UserEntryAdmin)

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('header', 'doc')

admin.site.register(UserAnswer, UserAnswerAdmin)
