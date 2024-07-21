from rest_framework import serializers
from rest_framework.views import APIView
from apps.accounts.models import CustomUser
from rest_framework.response import Response
from exceptions.restapi import CustomAPIException
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

# local imports 
from helper.serializers import inline_serializer
from helper.constant import WEEK_DAYS, SHIFT_INTERCHANGE_REQUEST_STATUSV2
from apps.attendance.services import *
from .serializers import *

class StaffShiftScheduleAPI(APIView):
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        employee_id = serializers.CharField()
        shift = inline_serializer(fields={
            "day": serializers.ChoiceField(choices=WEEK_DAYS),
            "shift_start": serializers.TimeField(format='%H:%M', input_formats=['%H:%M']),
            "shift_end": serializers.TimeField(format='%H:%M', input_formats=['%H:%M']),
        })

    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        print(serializer.data)
        shift = assign_staff_shift(manager=request.user, **serializer.data)
        output_serializer = ShiftSerializer(shift)
        return Response({"data": output_serializer.data})


class AssignStaffWeeklyOffAPI(APIView):
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        employee_id = serializers.CharField()
        weekly_off = serializers.ListField(child=serializers.ChoiceField(choices=WEEK_DAYS))

        def validate(self, data):
            weekly_off_days = data.get('weekly_off', [])
            if len(weekly_off_days) != 2:
                raise serializers.ValidationError("You must specify exactly two days for weekly off.")
            return data
        

    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")

        staff_member = assign_staff_weekly_off(manager=request.user, **serializer.data)
        output_serializer = StaffMemberSerializer(staff_member, context={"request": request})
        return Response({"data": output_serializer.data})


# staff user APIS.
class StaffMemberAssignedShifts(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args,  **kwargs):
        shifts = get_staff_assigned_shifts(staff_user=request.user)
        output_serializer = ShiftSerializer(shifts, many=True,  context={"request": request})
        response = {
            "count": len(output_serializer.data),
            "data": output_serializer.data
            }
        return Response(response)


class MarkStaffAttendanceAPI(APIView):
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        image = serializers.ImageField()
        
    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        attendance = mark_attendance( staff_user=request.user, **serializer.validated_data )
        output_serializer = AttendanceSerializer(attendance, context={"request": request})
        return Response({"data": output_serializer.data})


class RequestForInterchangeShiftsAPI(APIView):
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        target_email = serializers.EmailField()
        requester_shift_id = serializers.IntegerField()
        target_shift_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        shift_interchange_request = request_shift_interchange( staff_user=request.user, **serializer.validated_data )
        output_serializer = ShiftInterchangeRequestSerializer(shift_interchange_request, context={"request": request})
        return Response({"data": output_serializer.data})


class ShiftInterchangeRequestListAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, **kwargs):
        shift_interchange_request = get_shift_interchange_requests( staff_user=request.user )
        output_serializer = ShiftInterchangeRequestSerializer( shift_interchange_request, many=True, context={"request": request} )
        return Response({"data": output_serializer.data})

class ShiftInterchangeRequestStatusUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    
    class InputSerializer(serializers.Serializer):
        request_id = serializers.IntegerField()
        status = serializers.ChoiceField(choices=SHIFT_INTERCHANGE_REQUEST_STATUSV2)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        shift_interchange_request = update_shift_interchange_request_status( staff_user=request.user, **serializer.validated_data )
        output_serializer = ShiftInterchangeRequestSerializer(shift_interchange_request, context={"request": request})
        return Response({"data": output_serializer.data})

        