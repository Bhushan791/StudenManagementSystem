from django.contrib import admin
from .models import Course, Student

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'get_student_count', 'created_at']
    list_filter = ['created_at', 'duration']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_student_count(self, obj):
        return obj.get_student_count()
    get_student_count.short_description = 'Students Enrolled'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'email', 'course', 'enrollment_date']
    list_filter = ['course', 'enrollment_date', 'age']
    search_fields = ['name', 'email', 'course__name']
    readonly_fields = ['enrollment_date', 'updated_at']
    list_select_related = ['course']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'age', 'email')
        }),
        ('Academic Information', {
            'fields': ('course',)
        }),
        ('Timestamps', {
            'fields': ('enrollment_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
