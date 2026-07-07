from django.contrib import admin
from embedded.models import SensorData, SystemEvent

admin.site.register(SensorData)

@admin.register(SystemEvent)
class SystemEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'event_type', 'created', 'seen']
    list_filter = ['level', 'event_type', 'seen', 'created']
    search_fields = ['title', 'message']
    readonly_fields = ['created']
    ordering = ['-created']
    actions = ['mark_as_seen']
    
    def mark_as_seen(self, request, queryset):
        queryset.update(seen=True)
    mark_as_seen.short_description = "علامت‌گذاری به عنوان دیده شده"