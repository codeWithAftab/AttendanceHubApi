from django.contrib import admin
from .models import Shift, Attendance


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
