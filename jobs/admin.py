from django.contrib import admin
from .models import Category, Job, JobApplication


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'category', 'job_type', 'price', 'location', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'job_type', 'category', 'created_at']
    search_fields = ['title', 'description', 'location', 'employer__username']
    readonly_fields = ['slug', 'views_count', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Негизги маалымат', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Жумуш деталдары', {
            'fields': ('job_type', 'price', 'location', 'contact_phone')
        }),
        ('Жумуш берүүчү', {
            'fields': ('employer',)
        }),
        ('Статус жана медиа', {
            'fields': ('status', 'image')
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employer', 'category')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'created_at']
    list_filter = ['created_at']
    search_fields = ['applicant__username', 'job__title', 'message']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('applicant', 'job')
