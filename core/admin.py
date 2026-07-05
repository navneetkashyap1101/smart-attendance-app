from django.contrib import admin
from .models import Teacher, Student, ClassSession, Attendance


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'phone')
    search_fields = ('user__username', 'subject')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'user', 'class_name', 'attendance_percentage')
    search_fields = ('roll_no', 'user__username', 'class_name')
    list_filter = ('class_name',)


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'subject', 'teacher', 'date', 'is_active')
    list_filter = ('class_name', 'date', 'is_active')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'marked_at')
    list_filter = ('status', 'session__date')
    search_fields = ('student__roll_no',)
