from django.contrib import admin
from .models import Shift, Attendance, ShiftInterchangeRequest


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('staff_member', 'day', 'shift_start', 'shift_end')
    list_filter = ('day', 'staff_member')
    search_fields = ('staff_member__employee_id', 'day')
    ordering = ('day', 'shift_start')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff_member', 'date', 'timestamp', 'image')
    list_filter = ('date', 'staff_member')
    search_fields = ('staff_member__employee_id', 'date')
    readonly_fields = ('timestamp',)

@admin.register(ShiftInterchangeRequest)
class ShiftInterchangeRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'target', 'requester_shift', 'target_shift', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('requester__user__email', 'target__user__email', 'requester_shift__name', 'target_shift__name')
    ordering = ('-created_at',)

    # Optionally, customize the form display if needed
    fieldsets = (
        (None, {
            'fields': ('requester', 'target', 'requester_shift', 'target_shift', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')