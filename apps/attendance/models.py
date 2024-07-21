from apps.accounts.models import StaffManager, StaffMember, CustomUser
from django.db import models
from helper.constant import USER_ROLES, WEEK_DAYS, SHIFT_INTERCHANGE_REQUEST_STATUS

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


class ShiftInterchangeRequest(models.Model):
    requester = models.ForeignKey(StaffMember, related_name='requested_interchanges', on_delete=models.CASCADE)
    target = models.ForeignKey(StaffMember, related_name='received_interchanges', on_delete=models.CASCADE)
    requester_shift = models.ForeignKey('Shift', related_name='requester_shift', on_delete=models.CASCADE)
    target_shift = models.ForeignKey('Shift', related_name='target_shift', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=SHIFT_INTERCHANGE_REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"requester : {self.requester}"