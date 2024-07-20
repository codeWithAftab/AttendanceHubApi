from rest_framework import serializers
from apps.accounts.api.serializers import *

class ShiftSerializer(serializers.Serializer):
    staff_member_id = serializers.IntegerField()
    day = serializers.CharField(max_length=10)
    shift_start = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    shift_end = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])


class AttendanceSerializer(serializers.Serializer):
    staff_member_id = serializers.IntegerField()
    date = serializers.DateField()
    timestamp = serializers.DateTimeField(read_only=True)
    image = serializers.ImageField()
