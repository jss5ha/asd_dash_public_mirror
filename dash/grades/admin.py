from django.contrib import admin
from .models import course, assignment, assType
# Register your models here.

class AssignmentTypeInLine(admin.TabularInline):
    model = assType
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course_name']}),
    ]
    inlines = [AssignmentTypeInLine]
    # list_display = ('course_name')
    search_fields = ['course_name']
admin.site.register(course, CourseAdmin)