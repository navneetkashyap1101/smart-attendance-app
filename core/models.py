from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.subject})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_no = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.roll_no} - {self.user.get_full_name() or self.user.username}"

    def attendance_percentage(self):
        total = self.attendance_records.count()
        if total == 0:
            return 0
        present = self.attendance_records.filter(status='Present').count()
        return round((present / total) * 100, 2)


class ClassSession(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='sessions')
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.class_name} - {self.subject} ({self.date})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'session')

    def __str__(self):
        return f"{self.student.roll_no} - {self.session} - {self.status}"
