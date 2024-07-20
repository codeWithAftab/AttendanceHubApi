from django.urls import path, include
from . import views

urlpatterns = [
    path('staff/shift/schedule/', views.StaffShiftScheduleAPI.as_view()),
    path('staff/weekly-off/assign/', views.AssignStaffWeeklyOffAPI.as_view()),
    path('staff/assigned/shifts/', views.StaffMemberAssignedShifts.as_view()),
    path('staff/attendance/mark/', views.MarkStaffAttendanceAPI.as_view()),
]
