from django.contrib import admin
from .models import course, assignment, assType
# Register your models here.
# from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
class AssignmentInLine(admin.TabularInline):
    model = assignment

class AssignmentTypeInLine(admin.TabularInline):
    model = assType
    inlines = [AssignmentInLine,]

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course_name']}),
        ('Course Grade', {'fields': ['course_grade']}),
    ]
    inlines = [AssignmentInLine,]
    # list_display = ('course_name')
    search_fields = ['course_name']
admin.site.register(course, CourseAdmin)