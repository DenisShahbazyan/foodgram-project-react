from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email', 'is_staff')
    list_editable = ('username', 'first_name',
                     'last_name', 'email', 'is_staff')
    search_fields = ('username', 'email', 'is_staff')
    list_filter = ('email', 'username')
    filter_horizontal = ('subscribe',)
