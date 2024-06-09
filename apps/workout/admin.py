from django.contrib import admin
from .models import BodyPart, Exercise

class BodyPartAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description',)


admin.site.register(BodyPart, BodyPartAdmin)
admin.site.register(Exercise, ExerciseAdmin)
