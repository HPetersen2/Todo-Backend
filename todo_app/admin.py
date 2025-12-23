from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date', 'creator', 'created_at', 'updated_at')
    
    list_filter = ('status', 'priority', 'due_date', 'creator')
    
    search_fields = ('title', 'description', 'creator__username')
    
    fields = ('title', 'description', 'status', 'priority', 'due_date', 'completed_at', 'creator')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status', 'priority')
        }),
        ('Scheduling', {
            'fields': ('due_date', 'completed_at')
        }),
        ('Ownership', {
            'fields': ('creator',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # 'collapse' macht die Timestamps zusammenklappbar
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

    def get_status_display(self, obj):
        return obj.get_status_display()
    get_status_display.short_description = 'Status'

    def get_priority_display(self, obj):
        return obj.get_priority_display()
    get_priority_display.short_description = 'Priority'

admin.site.register(Todo, TodoAdmin)
