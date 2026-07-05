from rest_framework import serializers
from .models import Student, Teacher, ClassSession, Attendance


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.SerializerMethodField()
    attendance_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'username', 'full_name', 'roll_no', 'class_name', 'phone', 'attendance_percentage']

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_attendance_percentage(self, obj):
        return obj.attendance_percentage()


class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'username', 'full_name', 'subject', 'phone']

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class ClassSessionSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = ClassSession
        fields = ['id', 'teacher', 'teacher_name', 'class_name', 'subject', 'date', 'created_at', 'is_active']
        read_only_fields = ['date', 'created_at']


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_no', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'student_roll', 'session', 'status', 'marked_at']
        read_only_fields = ['marked_at']
