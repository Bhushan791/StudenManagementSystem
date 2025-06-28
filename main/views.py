from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from .models import Course, Student
from .forms import AdminLoginForm, CourseForm, StudentForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

# Custom Error Views
def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)

# Authentication Views
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')

@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    total_courses = Course.objects.count()
    total_students = Student.objects.count()
    recent_students = Student.objects.order_by('-enrollment_date')[:5]
    
    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'recent_students': recent_students,
    }
    return render(request, 'admin_dashboard.html', context)

# Course Views
@login_required
@user_passes_test(is_admin)
def view_courses(request):
    search_query = request.GET.get('search', '')
    courses = Course.objects.all()
    
    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(courses, 10)  # 10 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_courses': courses.count()
    }
    return render(request, 'courses/view_courses.html', context)

@login_required
@user_passes_test(is_admin)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('view_courses')
    else:
        form = CourseForm()
    
    return render(request, 'courses/add_course.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('view_courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/update_course.html', {'form': form, 'course': course})

@login_required
@user_passes_test(is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_name = course.name
    course.delete()
    messages.success(request, f'Course "{course_name}" deleted successfully!')
    return redirect('view_courses')

# Student Views
@login_required
@user_passes_test(is_admin)
def view_students(request):
    search_query = request.GET.get('search', '')
    course_filter = request.GET.get('course', '')
    students = Student.objects.select_related('course')
    
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(course__name__icontains=search_query)
        )
    
    if course_filter:
        students = students.filter(course_id=course_filter)
    
    paginator = Paginator(students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    courses = Course.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'course_filter': course_filter,
        'courses': courses,
        'total_students': students.count()
    }
    return render(request, 'students/view_students.html', context)

@login_required
@user_passes_test(is_admin)
def add_student(request):
    if not Course.objects.exists():
        messages.warning(request, 'Please add at least one course before adding students.')
        return redirect('add_course')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('view_students')
    else:
        form = StudentForm()
    
    return render(request, 'students/add_student.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('view_students')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/update_student.html', {'form': form, 'student': student})

@login_required
@user_passes_test(is_admin)
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student_name = student.name
    student.delete()
    messages.success(request, f'Student "{student_name}" deleted successfully!')
    return redirect('view_students')
