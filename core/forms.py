from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher


class StudentSignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    roll_no = forms.CharField(max_length=20)
    class_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=15, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_roll_no(self):
        roll_no = self.cleaned_data['roll_no']
        if Student.objects.filter(roll_no=roll_no).exists():
            raise forms.ValidationError("Roll number already registered.")
        return roll_no

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            password=data['password'],
        )
        student = Student.objects.create(
            user=user,
            roll_no=data['roll_no'],
            class_name=data['class_name'],
            phone=data.get('phone', ''),
        )
        return student


class TeacherSignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    subject = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            password=data['password'],
        )
        teacher = Teacher.objects.create(
            user=user,
            subject=data['subject'],
            phone=data.get('phone', ''),
        )
        return teacher


class MarkAttendanceForm(forms.Form):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]
    student_id = forms.IntegerField(widget=forms.HiddenInput)
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)
