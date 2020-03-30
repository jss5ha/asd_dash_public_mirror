from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from .models import course, assignment, assType, pointAssignment
# Register your models here.

class PointAssignmentInLine(NestedTabularInline):
    model = pointAssignment

class AssignmentInLine(NestedTabularInline):
    model = assignment

class AssignmentTypeInLine(NestedTabularInline):
    model = assType
    inlines = [AssignmentInLine,]

class CourseAdmin(NestedModelAdmin):
    fieldsets = [
        (None, {'fields': ['course_name']}),
        ('Course Grade', {'fields': ['course_grade']}),
        ('User', {'fields':['owner']}),
    ]
    inlines = [AssignmentTypeInLine, PointAssignmentInLine,]
    # list_display = ('course_name')
    search_fields = ['course_name']


admin.site.register(course, CourseAdmin)
