from django.contrib import admin
from .models import FitnessCentre, FitnessCentreMembership, Membership

@admin.register(FitnessCentre)
class FitnessCentreAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = ('name', 'phone_number', 'address', 'zip_code', 'created_on', 'updated_on')
    search_fields = ('name', 'phone_number', 'address', 'zip_code')
    list_filter = ('created_on', 'updated_on')

@admin.register(FitnessCentreMembership)
class FitnessCentreMembershipAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = ('fitness_centre', 'title', 'membership_type', 'price', 'created_on', 'updated_on')
    search_fields = ('fitness_centre__name', 'title', 'membership_type')
    list_filter = ('membership_type', 'created_on', 'updated_on')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ( 'membership_type', 'start_date', 'end_date', 'active_status', 'created_on', 'updated_on')
    search_fields = ('member__username', 'membership_type__title', 'membership_type__fitness_centre__name')
    list_filter = ( 'membership_type__membership_type', 'created_on', 'updated_on')
    readonly_fields = ["end_date"]
    
    def active_status(self, obj):
        return obj.is_active
    
    active_status.boolean = True  # This makes the boolean appear as a tick or cross icon
    active_status.short_description = 'Is Active'  # This sets the column name in the admin

    