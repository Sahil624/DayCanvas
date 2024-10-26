from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'age', 'interests']
    search_fields = ['user__username', 'name', 'interests']
    list_filter = ['age']
    readonly_fields = ['user']