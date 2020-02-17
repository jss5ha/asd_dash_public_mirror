from django.contrib import admin
from .models import course, assignment, assType
# Register your models here.

class AssignmentInLine(admin.TabularInline):
    model = assignment
    extra = 3

class AssignmentTypeInLine(admin.TabularInline):
    model = assType
    inlines = [AssignmentInLine]

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course_name']}),
    ]
    inlines = [AssignmentTypeInLine]
    # list_display = ('course_name')
    search_fields = ['course_name']
admin.site.register(course, CourseAdmin)