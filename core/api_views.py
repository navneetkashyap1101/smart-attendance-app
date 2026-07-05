from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Teacher, ClassSession, Attendance
from .serializers import (
    StudentSerializer, TeacherSerializer,
    ClassSessionSerializer, AttendanceSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['class_name']

    def get_queryset(self):
        qs = super().get_queryset()
        class_name = self.request.query_params.get('class_name')
        if class_name:
            qs = qs.filter(class_name=class_name)
        return qs


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassSessionViewSet(viewsets.ModelViewSet):
    queryset = ClassSession.objects.all().order_by('-created_at')
    serializer_class = ClassSessionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-marked_at')
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        student_id = self.request.query_params.get('student')
        session_id = self.request.query_params.get('session')
        if student_id:
            qs = qs.filter(student_id=student_id)
        if session_id:
            qs = qs.filter(session_id=session_id)
        return qs

    @action(detail=False, methods=['get'])
    def my_attendance(self, request):
        """Returns attendance records for the logged-in student."""
        if not hasattr(request.user, 'student_profile'):
            return Response({'error': 'Not a student account'}, status=403)
        student = request.user.student_profile
        records = self.get_queryset().filter(student=student)
        serializer = self.get_serializer(records, many=True)
        return Response({
            'percentage': student.attendance_percentage(),
            'records': serializer.data
        })
