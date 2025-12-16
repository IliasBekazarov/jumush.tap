from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'location', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Колдонуучу', {
            'fields': ('user', 'user_type')
        }),
        ('Байланыш маалыматы', {
            'fields': ('phone', 'location')
        }),
        ('Кошумча маалымат', {
            'fields': ('bio', 'avatar')
        }),
        ('Убакыт маалыматы', {
            'fields': ('created_at', 'updated_at')
        }),
    )
