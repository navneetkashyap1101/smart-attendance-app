from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Student, Teacher, ClassSession, Attendance
from .forms import StudentSignUpForm, TeacherSignUpForm


# ---------- Auth Views ----------

def signup_choice(request):
    return render(request, 'core/signup_choice.html')


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            student = form.save()
            login(request, student.user)
            messages.success(request, "Account created successfully!")
            return redirect('student_dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'core/student_signup.html', {'form': form})


def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            login(request, teacher.user)
            messages.success(request, "Account created successfully!")
            return redirect('teacher_dashboard')
    else:
        form = TeacherSignUpForm()
    return render(request, 'core/teacher_signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_redirect(request):
    if hasattr(request.user, 'teacher_profile'):
        return redirect('teacher_dashboard')
    elif hasattr(request.user, 'student_profile'):
        return redirect('student_dashboard')
    return redirect('login')


# ---------- Student Views ----------

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    records = student.attendance_records.select_related('session').order_by('-marked_at')
    context = {
        'student': student,
        'records': records,
        'percentage': student.attendance_percentage(),
    }
    return render(request, 'core/student_dashboard.html', context)


# ---------- Teacher Views ----------

@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    sessions = teacher.sessions.order_by('-created_at')[:10]
    context = {
        'teacher': teacher,
        'sessions': sessions,
    }
    return render(request, 'core/teacher_dashboard.html', context)


@login_required
def create_session(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        session = ClassSession.objects.create(
            teacher=teacher, class_name=class_name, subject=subject
        )
        return redirect('mark_attendance', session_id=session.id)
    return render(request, 'core/create_session.html')


@login_required
def mark_attendance(request, session_id):
    session = get_object_or_404(ClassSession, id=session_id, teacher__user=request.user)
    students = Student.objects.filter(class_name=session.class_name)

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'Absent')
            Attendance.objects.update_or_create(
                student=student, session=session,
                defaults={'status': status}
            )
        messages.success(request, "Attendance marked successfully!")
        return redirect('session_report', session_id=session.id)

    # pre-fill existing attendance if any
    existing = {a.student_id: a.status for a in session.attendance_records.all()}
    student_list = [(s, existing.get(s.id, 'Present')) for s in students]

    context = {'session': session, 'student_list': student_list}
    return render(request, 'core/mark_attendance.html', context)


@login_required
def session_report(request, session_id):
    session = get_object_or_404(ClassSession, id=session_id, teacher__user=request.user)
    records = session.attendance_records.select_related('student').order_by('student__roll_no')
    total = records.count()
    present = records.filter(status='Present').count()
    context = {
        'session': session,
        'records': records,
        'total': total,
        'present': present,
        'absent': total - present,
        'percentage': round((present / total) * 100, 2) if total else 0,
    }
    return render(request, 'core/session_report.html', context)
