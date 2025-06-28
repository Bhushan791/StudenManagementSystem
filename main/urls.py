"""
Main App URL Configuration
All URLs for the Student Management System functionality
"""
from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # AUTHENTICATION URLS
    # ==========================================
    path('', views.admin_login_view, name='admin_login'),
    path('login/', views.admin_login_view, name='admin_login_page'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
    
    # ==========================================
    # DASHBOARD URLS
    # ==========================================
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # ==========================================
    # COURSE MANAGEMENT URLS
    # ==========================================
    path('courses/', views.view_courses, name='view_courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/update/<int:course_id>/', views.update_course, name='update_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    
    # ==========================================
    # STUDENT MANAGEMENT URLS
    # ==========================================
    path('students/', views.view_students, name='view_students'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/update/<int:student_id>/', views.update_student, name='update_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
]
