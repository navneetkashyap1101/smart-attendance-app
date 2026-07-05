from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from . import api_views

router = DefaultRouter()
router.register(r'students', api_views.StudentViewSet)
router.register(r'teachers', api_views.TeacherViewSet)
router.register(r'sessions', api_views.ClassSessionViewSet)
router.register(r'attendance', api_views.AttendanceViewSet)

urlpatterns = [
    # Auth pages
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_choice, name='signup_choice'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Student
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # Teacher
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/session/create/', views.create_session, name='create_session'),
    path('teacher/session/<int:session_id>/mark/', views.mark_attendance, name='mark_attendance'),
    path('teacher/session/<int:session_id>/report/', views.session_report, name='session_report'),

    # REST API
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
