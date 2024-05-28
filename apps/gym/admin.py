from django.contrib import admin
from .models import FitnessCentre, FitnessCentreMembership, Membership

@admin.register(FitnessCentre)
class FitnessCentreAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address', 'zip_code', 'created_on', 'updated_on')
    search_fields = ('name', 'phone_number', 'address', 'zip_code')
    list_filter = ('created_on', 'updated_on')

@admin.register(FitnessCentreMembership)
class FitnessCentreMembershipAdmin(admin.ModelAdmin):
    list_display = ('fitness_centre', 'title', 'membership_type', 'price', 'created_on', 'updated_on')
    search_fields = ('fitness_centre__name', 'title', 'membership_type')
    list_filter = ('membership_type', 'created_on', 'updated_on')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ( 'membership_type', 'start_date', 'end_date', 'is_active', 'created_on', 'updated_on')
    search_fields = ('member__username', 'membership_type__title', 'membership_type__fitness_centre__name')
    list_filter = ('is_active', 'membership_type__membership_type', 'created_on', 'updated_on')
