from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'created_by', 'status', 'due_date', 'worked_hours', 'created_at')
    list_filter = ('status', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'assigned_to', 'created_by', 'due_date', 'status')
        }),
        ('Completion Details', {
            'fields': ('completion_report', 'worked_hours'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == 'superadmin':
            return qs
        elif request.user.role == 'admin':
            return qs.filter(assigned_to__assigned_admin=request.user) | qs.filter(created_by=request.user)
        return qs.filter(assigned_to=request.user)
