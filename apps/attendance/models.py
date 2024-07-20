from apps.accounts.models import StaffManager, StaffMember, CustomUser
from django.db import models
from helper.constant import USER_ROLES, WEEK_DAYS

class Shift(models.Model):
    staff_member = models.ForeignKey(StaffMember, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=WEEK_DAYS)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    
    class Meta:
        unique_together = ["staff_member", "day"]


class Attendance(models.Model):
    staff_member = models.ForeignKey(StaffMember, on_delete=models.CASCADE)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='attendance_images/')

    class Meta:
        unique_together = ["staff_member", "date"]
