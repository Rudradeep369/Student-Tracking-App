from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Batch,Teacher, Payment, Parent, Achievement, StudyMaterial
from .forms import StudentForm, BatchForm,TeacherForm, PaymentForm, ParentForm, AchievementForm, StudyMaterialForm
from django.contrib import messages
from django.views.generic import DetailView
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.db import models
from decimal import Decimal
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import os


# Home Page with Student List and Search

def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')    
        return redirect('index')
    context = {}
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    context['form'] = LoginForm()
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required(login_url='login')
def index(request):
    search_query = request.GET.get("search", "")
    per_page = int(request.GET.get("per_page", 10))  # Default 10 items per page
    students = Student.objects.all()

    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(board__icontains=search_query) |
            Q(student_class__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(students, per_page)  # Use dynamic per_page value
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_students = students.count()
    cbse_students = students.filter(board='CBSE').count()
    wbbse_students = students.filter(board='WBBSE').count()
    icse_students = students.filter(board='ICSE').count()
    wbchse_students = students.filter(board='WBCHSE').count()
    isc_students = students.filter(board='ISC').count()

    context = {
        'students': page_obj,  # Use paginated students
        'page_obj': page_obj,  # Add page object for pagination controls
        'total_students': total_students,
        'cbse_students': cbse_students,
        'wbbse_students': wbbse_students,
        'icse_students': icse_students,
        'wbchse_students': wbchse_students,
        'isc_students': isc_students,
        'search': search_query,
        'batch_form': BatchForm(),
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def filter_students(request):
    print(request.GET)
    per_page = int(request.GET.get("per_page", 10))  # Default 10 items per page
    
    if request.GET.get("Board") or request.GET.get("Class") or request.GET.get("Subject"):
        filters = {}
    
        board = request.GET.get("Board")
        student_class = request.GET.get("Class")
        subject = request.GET.get("Subject")
        
        if board:
            filters['board'] = board
        if student_class:
            filters['student_class'] = int(student_class)
        if subject:
            filters['subject__icontains'] = subject
        
        students = Student.objects.filter(**filters)
        
        # Pagination for filtered results
        paginator = Paginator(students, per_page)  # Use dynamic per_page value
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # print("Students:", students)
        context = {
            'students': page_obj,  # Use paginated students
            'page_obj': page_obj,  # Add page object for pagination controls
            'total_students': students.count(),
            'cbse_students': students.filter(board='CBSE').count(),
            'wbbse_students': students.filter(board='WBBSE').count(),
            'icse_students': students.filter(board='ICSE').count(),
            'search': request.GET.get('search', ''),
            'board_filter': board,
            'class_filter': student_class,
            'subject': subject,
            'batch_form': BatchForm(),
        }
    else:
        students = Student.objects.all()
        
        # Pagination for all students
        paginator = Paginator(students, per_page)  # Use dynamic per_page value
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'students': page_obj,  # Use paginated students
            'page_obj': page_obj,  # Add page object for pagination controls
            'total_students': Student.objects.count(),
            'cbse_students': Student.objects.filter(board='CBSE').count(),
            'wbbse_students': Student.objects.filter(board='WBBSE').count(),
            'icse_students': Student.objects.filter(board='ICSE').count(),
            'search': request.GET.get('search', ''),
            'batch_form': BatchForm(),
        }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def all_students(request):
    """View to display all students with search and filtering options"""
    search_query = request.GET.get("search", "")
    board_filter = request.GET.get("board", "")
    class_filter = request.GET.get("class", "")
    
    students = Student.objects.all()
    
    # Apply search filter
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(board__icontains=search_query) |
            Q(student_class__icontains=search_query) |
            Q(parent_name__icontains=search_query)
        )
    
    # Apply board filter
    if board_filter:
        students = students.filter(board=board_filter)
    
    # Apply class filter
    if class_filter:
        students = students.filter(student_class=class_filter)
    
    # Get unique values for filter dropdowns
    boards = Student.objects.values_list('board', flat=True).distinct()
    classes = Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class')
    
    total_students = students.count()
    
    context = {
        'students': students,
        'total_students': total_students,
        'search': search_query,
        'board_filter': board_filter,
        'class_filter': class_filter,
        'boards': boards,
        'classes': classes,
        'student_form': StudentForm(),  # Add student form for potential modal use
    }
    return render(request, 'all_students.html', context)


@login_required(login_url='login')
def add_student(request):
    """View to add a new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.name}" has been added successfully!')
            return redirect('all_students')
        else:
            # If form has errors, show them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Student'
    }
    return render(request, 'add_student.html', context)
        
# Student Profile Page
@login_required(login_url='login')
def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    batches = Batch.objects.filter(students=student)
    payments = Payment.objects.filter(student=student).order_by('-updated_date')
    context = {
        'student': student,
        'batches': batches,
        'payments': payments,
    }
    parent=Parent.objects.filter(child=student)
    if parent:
        context['parent']=parent[0]
    else:
        context['parent']=parent
        

    return render(request, 'student_profile.html', context)

# Create a New Batch
@login_required(login_url='login')
def create_batch(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        print(request.method)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, "Batch created successfully!")
            return redirect('view_batches')
        else:
            print(form.errors)
            messages.error(request, "Error creating batch. Please try again.")
    else:
        form = BatchForm()
    return redirect('index')
    # return render(request, 'wrong.html', {'form': form})

# View All Batches
@login_required(login_url='login')
def view_batches(request):
    search_query = request.GET.get('search', '')

    if search_query:
        batches = Batch.objects.filter(
            Q(subject_name__icontains=search_query) |
            Q(class_level__icontains=search_query) |
            Q(batch_day__icontains=search_query) 
        )
    else:
        batches = Batch.objects.all()

    return render(request, 'view_batches.html', {'batches': batches})

# Batch Detail View
class BatchDetailView(LoginRequiredMixin, DetailView):
    model = Batch
    template_name = 'batch_detail.html'
    context_object_name = 'batch'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search_batch_student'):
            search_query = self.request.GET.get('search_batch_student')
            # students = Student.objects.filter(
            #     Q(name__icontains=search_query) |
            #     Q(phone_number__icontains=search_query) |
            #     Q(board__icontains=search_query) |
            #     Q(student_class__icontains=search_query) 
            # )
            # context['students'] = students.filter(batches=self.object)

            students = Student.objects.filter(id__in=self.object.students.all()).filter(
                Q(name__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(board__icontains=search_query) |
                Q(student_class__icontains=search_query) 
            )
            context['students'] = students
            
        else:
            context['students'] = self.object.students.all()
        
        if self.request.GET.get('search_remaining_student'):
            search_query = self.request.GET.get('search_remaining_student')
            context['remaining_students'] = Student.objects.exclude(id__in=self.object.students.all()).filter(
                Q(name__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(board__icontains=search_query) |
                Q(student_class__icontains=search_query) 
            )
        else:
            context['remaining_students'] = Student.objects.exclude(id__in=self.object.students.all())
        
        # Add teacher-related context
        context['assigned_teachers'] = self.object.teachers.all()
        context['available_teachers'] = Teacher.objects.exclude(id__in=self.object.teachers.all())
        
        context['student_form'] = StudentForm()
        return context

# Add Existing Students to a Batch
@login_required(login_url='login')
def add_existing_students(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        student_ids = request.POST.getlist('existing_students')
        existing_students = batch.students.all().values_list('id', flat=True)
        new_students = [Student.objects.get(id=id) for id in student_ids if int(id) not in existing_students]
        duplicate_students = [Student.objects.get(id=id) for id in student_ids if int(id) in existing_students]
        
        if new_students:
            batch.students.add(*new_students)
            messages.success(request, "Students successfully added to the batch.")
        if duplicate_students:
            messages.info(request, "Some students are already in this batch.")
    
    return redirect('batch_detail', pk=pk)

# Add a New Student to a Batch
@login_required(login_url='login')
def add_new_student(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student = form.save()
            batch.students.add(new_student)
            messages.success(request, "New student added to the batch.")
            return redirect('batch_detail', pk=pk)
        else:
            # print(form.errors)
            messages.error(request, "Error adding student. Please try again.")
            return redirect('batch_detail', pk=pk)

    else:
        form = StudentForm()
    return redirect('batch_detail', pk=pk)
    # return render(request, 'add_new_student.html', {'form': form})

# Edit Batch Details
@login_required(login_url='login')
def edit_batch(request, id):
    batch = get_object_or_404(Batch, id=id)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch updated successfully!')
            return redirect('view_batches')
        else:
            messages.error(request, 'Error updating batch. Please try again.')
    else:
        form = BatchForm(instance=batch)
    return render(request, 'edit_batch.html', {'form': form, 'batch': batch})

# Delete a Batch
@login_required(login_url='login')
def delete_batch(request, id):
    batch = get_object_or_404(Batch, id=id)
    if request.method == "POST":
        batch.delete()
        messages.success(request, 'Batch deleted successfully!')
        return redirect('view_batches')
    return render(request, 'confirm_delete.html', {'batch': batch})

# Remove a Student from a Batch
@login_required(login_url='login')
def remove_student_from_batch(request, batch_id, student_id):
    batch = get_object_or_404(Batch, id=batch_id)
    student = get_object_or_404(Student, id=student_id)
    batch.students.remove(student)
    messages.success(request, f'{student.name} has been removed from the batch.')
    return redirect('batch_detail', pk=batch.id)

# Edit Student Profile
@login_required(login_url='login')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student profile updated successfully!')
            return redirect('student_profile', student_id=student.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form, 'student': student})

# Delete Student Profile
@login_required(login_url='login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student profile deleted successfully!')
        return redirect('index')
    return render(request, 'confirm_delete_student.html', {'student': student})

# Add a Teacher/Instructor
@login_required(login_url='login')
def add_teacher(request):
    search_query = request.GET.get('search', '')  # Get the search query

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully!')
            return redirect('add_teacher')  # Redirect to the same page after saving
    else:
        form = TeacherForm()

    # Filter teachers based on search query
    if search_query:
        teachers = Teacher.objects.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(subject_teaches__icontains=search_query) |
            Q(qualification__icontains=search_query)
        )
    else:
        teachers = Teacher.objects.all()

    return render(request, 'add_teacher.html', {'form': form, 'teachers': teachers, 'search': search_query})


# Edit teacher view
@login_required(login_url='login')
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
        # form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            if 'profile_image' in request.FILES:
                # Delete the old image if a new one is uploaded
                if teacher.profile_image:
                    if os.path.isfile(teacher.profile_image.url):
                        os.remove(teacher.profile_image.url)
            form.save()
            messages.success(request, 'Teacher table updated successfully!')
            return redirect('add_teacher')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'edit_teacher.html', {'form': form})


# Delete teacher view
@login_required(login_url='login')
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.delete()  # Signal handler will automatically delete the image
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('all_teachers')
    # For GET requests, redirect to teacher list or show confirmation
    return redirect('all_teachers')


# def clear_previous_due(student_id, due_amount):
#     student = get_object_or_404(Student, id=student_id)
#     payments = Payment.objects.filter(student=student)

@login_required(login_url='login')
def payment_record(request, student_id):
    if request.method == "POST":
        
        student = get_object_or_404(Student, id=student_id)
        amount = Decimal(request.POST['payment'])
        payment_method = request.POST.get('payment_method')
        payment_date = request.POST.get('payment_date')
        payment_month = request.POST.getlist('payment_months')
        
        # Ensure payment_month values are strings
        payment_month = [str(month) for month in payment_month]

        student_fees = Decimal(student.fees)
        due_amount = (student_fees * len(payment_month)) - amount

        if due_amount < 0:
            due_amount = due_amount

        payment = Payment.objects.create(
            student=student,
            amount=amount,
            due_amount = due_amount,
            payment_method=payment_method,
            date=payment_date,
            months=payment_month
        )
        payment.save()

        messages.success(request, 'Payment recorded successfully!')
    return redirect("student_profile", student_id=student_id)

@login_required(login_url='login')
def all_payment(request):
    context = {}
    
    # Handle payment recording
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            student = get_object_or_404(Student, id=student_id)
            amount = Decimal(request.POST['payment'])
            payment_method = request.POST.get('payment_method')
            payment_date = request.POST.get('payment_date')
            payment_month = request.POST.getlist('payment_months')
            
            # Ensure payment_month values are strings
            payment_month = [str(month) for month in payment_month]

            student_fees = Decimal(student.fees)
            due_amount = (student_fees * len(payment_month)) - amount

            if due_amount < 0:
                due_amount = due_amount

            payment = Payment.objects.create(
                student=student,
                amount=amount,
                due_amount=due_amount,
                payment_method=payment_method,
                date=payment_date,
                months=payment_month
            )
            payment.save()

            messages.success(request, f'Payment recorded successfully for {student.name}!')
            return redirect('all_payments')
    
    # Get pagination parameter
    per_page = int(request.GET.get("per_page", 10))  # Default 10 items per page
    
    payments = Payment.objects.all().order_by('-updated_date', '-date')

    # Date range filter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        payments = payments.filter(date__range=[start_date, end_date])

    # Search filter
    search_query = request.GET.get('search', '')
    if search_query:
        payments = payments.filter(
            Q(student__name__icontains=search_query) |
            Q(student__board__icontains=search_query) |
            Q(student__student_class__icontains=search_query) |
            Q(student__subject__icontains=search_query) |
            Q(payment_method__icontains=search_query)
        )

    # Calculate total amount for all filtered payments (before pagination)
    total_amount = payments.aggregate(total_amount=models.Sum('amount'))['total_amount']
    
    # Pagination
    paginator = Paginator(payments, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['payments'] = page_obj  # Use paginated payments
    context['page_obj'] = page_obj  # Add page object for pagination controls
    context['total_amount'] = total_amount if total_amount else 0
    context['total_payments'] = payments.count()  # Total count of filtered payments
    context['search'] = search_query  # Pass search query back to template to maintain the input
    context['start_date'] = request.GET.get('start_date', '')
    context['end_date'] = request.GET.get('end_date', '')
    context['students'] = Student.objects.all().order_by('name')  # For the payment form dropdown
    context['payment_form'] = PaymentForm()  # Add payment form to context
    return render(request, 'all_payments.html', context)


@login_required(login_url='login')
def edit_payment(request, id, std_id):
    payment = get_object_or_404(Payment, id=id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        prev_due = payment.due_amount
        if form.is_valid():
            form.save()

            if prev_due !=payment.due_amount:
                payment.modification= f"Due Modified {prev_due} -> {payment.due_amount}"
                payment.save() 
            else:
                print("due not modified")

            messages.success(request, 'Payment details updated successfully!')
            return redirect('student_profile', student_id=std_id)
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'edit_payment.html', {'form': form})

@login_required(login_url='login')
def add_parent(request, std_id):
    student = get_object_or_404(Student, id=std_id)
    context = {}
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            parent = form.save(commit=False)
            parent.child = student
            parent.save()
            messages.success(request, 'Parent details added successfully!')
            return redirect('student_profile', student_id=std_id)
    context['form'] = ParentForm()
    return render(request, 'add_parent.html', context)

@login_required(login_url='login')
def edit_parent(request, id, std_id):
    parent = get_object_or_404(Parent, id=id)
    student = get_object_or_404(Student, id=std_id)
    context ={}
    if request.method == "POST":
        form = ParentForm(request.POST, instance=parent)  # Ensure the form is bound to the existing parent instance
        if form.is_valid():
            parent = form.save(commit=False)
            parent.child = student
            parent.save()
            messages.success(request, 'Parent details updated successfully!')
            return redirect('student_profile', student_id=std_id)
    else:
        form = ParentForm(instance=parent) 
    context ['form']= form
    return render(request, 'add_parent.html', context)


def home(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers  # 'teachers' is the key to access in the template
    }
    context['achivements'] = Achievement.objects.all()
    print(context['achivements'])
    return render(request, "home.html", context)

def class_details(request):
    return render(request, "class_details.html")

def achievement(request):
    context = {}
    
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Achievement added successfully!')
            return redirect('achievement')
        else:
            # Form is not valid, add error messages
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = AchievementForm()

    achievements = Achievement.objects.all().order_by('-id')  # Fetch all achievements ordered by date
    
    # Calculate statistics
    total_achievements = achievements.count()
    students_with_90_plus = achievements.filter(score__gte=90).count()
    latest_score = achievements.first().score if achievements.exists() else 0
    unique_students = achievements.values('student_name').distinct().count()
    
    context['form'] = form
    context['achievements'] = achievements
    context['total_achievements'] = total_achievements
    context['students_with_90_plus'] = students_with_90_plus
    context['latest_score'] = latest_score
    context['unique_students'] = unique_students
    
    return render(request, 'achievement.html', context)


@login_required(login_url='login')
def edit_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id)
    
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES, instance=achievement)
        if form.is_valid():
            if 'image' in request.FILES:
                if achievement.image and achievement.image.path:
                    if os.path.isfile(achievement.image.path):
                        os.remove(achievement.image.path)
            form.save()
            messages.success(request, 'Achievement updated successfully!')
            return redirect('achievement')
    else:
        form = AchievementForm(instance=achievement)

    return render(request, 'edit_achievement.html', {'form': form})


@login_required(login_url='login')
def delete_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id)

    if request.method == 'POST':
        achievement.delete()  # Signal handler will automatically delete the image
        messages.success(request, 'Achievement deleted successfully!')
        return redirect('achievement')


# Teacher Assignment Views
@login_required(login_url='login')
def assign_teacher_to_batch(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        teacher_ids = request.POST.getlist('teachers_to_assign')
        if teacher_ids:
            teachers = Teacher.objects.filter(id__in=teacher_ids)
            batch.teachers.add(*teachers)
            teacher_names = [teacher.name for teacher in teachers]
            messages.success(request, f'Successfully assigned teachers: {", ".join(teacher_names)} to batch {batch.batch_name}')
        else:
            messages.warning(request, 'No teachers selected to assign.')
    return redirect('batch_detail', pk=pk)


@login_required(login_url='login')
def remove_teacher_from_batch(request, pk, teacher_id):
    batch = get_object_or_404(Batch, pk=pk)
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    
    if request.method == 'POST':
        batch.teachers.remove(teacher)
        messages.success(request, f'Successfully removed teacher {teacher.name} from batch {batch.batch_name}')
    
    return redirect('batch_detail', pk=pk)

# Teacher Profile Page
@login_required(login_url='login')
def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    batches = Batch.objects.filter(teachers=teacher)
    
    # Get all students from batches taught by this teacher
    students_in_batches = []
    for batch in batches:
        batch_students = batch.students.all()
        for student in batch_students:
            if student not in students_in_batches:
                students_in_batches.append(student)
    
    context = {
        'teacher': teacher,
        'batches': batches,
        'students': students_in_batches,
        'total_batches': batches.count(),
        'total_students': len(students_in_batches),
    }
    
    return render(request, 'teacher_profile.html', context)

# All Teachers Page
@login_required(login_url='login')
def all_teachers(request):
    teachers = Teacher.objects.all().order_by('name')
    
    # Add statistics for each teacher
    teachers_with_stats = []
    for teacher in teachers:
        batches = Batch.objects.filter(teachers=teacher)
        total_students = 0
        for batch in batches:
            total_students += batch.students.count()
        
        teachers_with_stats.append({
            'teacher': teacher,
            'total_batches': batches.count(),
            'total_students': total_students,
        })
    
    context = {
        'teachers_with_stats': teachers_with_stats,
        'total_teachers': teachers.count(),
    }
    
    return render(request, 'all_teachers.html', context)


# Add Study Material
@login_required(login_url='login')
def add_study_material(request):
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Study material added successfully!')
            return redirect('add_study_material')
        else:
            # Add debugging information
            print("Form errors:", form.errors)
            print("Form non-field errors:", form.non_field_errors())
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudyMaterialForm()
    
    # Get all study materials for display
    study_materials = StudyMaterial.objects.filter(is_active=True).order_by('-upload_date')[:5]
    
    context = {
        'form': form,
        'study_materials': study_materials,
    }
    return render(request, 'add_study_material.html', context)


# View All Study Materials
@login_required(login_url='login')
def all_study_materials(request):
    # Get filter parameters
    board_filter = request.GET.get('board', '')
    class_filter = request.GET.get('class', '')
    subject_filter = request.GET.get('subject', '')
    search_query = request.GET.get('search', '')
    
    # Start with all study materials
    study_materials = StudyMaterial.objects.filter(is_active=True)
    
    # Apply filters
    if board_filter:
        study_materials = study_materials.filter(board=board_filter)
    if class_filter:
        study_materials = study_materials.filter(class_level=class_filter)
    if subject_filter:
        study_materials = study_materials.filter(subject=subject_filter)
    if search_query:
        study_materials = study_materials.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    # Order by latest first
    study_materials = study_materials.order_by('-upload_date')
    
    # Get unique values for filters
    boards = StudyMaterial.objects.values_list('board', flat=True).distinct()
    classes = StudyMaterial.objects.values_list('class_level', flat=True).distinct().order_by('class_level')
    subjects = StudyMaterial.objects.values_list('subject', flat=True).distinct()
    
    context = {
        'study_materials': study_materials,
        'boards': boards,
        'classes': classes,
        'subjects': subjects,
        'board_filter': board_filter,
        'class_filter': class_filter,
        'subject_filter': subject_filter,
        'search_query': search_query,
        'total_materials': study_materials.count(),
    }
    return render(request, 'all_study_materials.html', context)


def study_materials_by_filter(request, class_level, subject, board):
    """
    View to display study materials filtered by class, subject, and board.
    Used when clicking on board buttons in class_details.html
    """
    # Filter study materials based on the parameters
    study_materials = StudyMaterial.objects.filter(
        class_level=class_level,
        subject=subject,
        board=board,
        is_active=True
    ).order_by('-upload_date')
    
    # Additional search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        study_materials = study_materials.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'study_materials': study_materials,
        'class_level': class_level,
        'subject': subject,
        'board': board,
        'search_query': search_query,
        'page_title': f'Class {class_level} {subject} - {board} Study Materials',
        'total_materials': study_materials.count(),
    }
    
    return render(request, 'study_materials_filtered.html', context)


from django.http import JsonResponse

def get_subjects_for_class(request):
    """
    AJAX view to return available subjects for a selected class level
    """
    class_level = request.GET.get('class_level')
    
    if not class_level:
        return JsonResponse({'subjects': []})
    
    try:
        class_level = int(class_level)
    except ValueError:
        return JsonResponse({'subjects': []})
    
    # Define subject choices based on class level
    if class_level in [5, 6, 7]:
        subjects = [
            {'value': 'Science', 'label': 'Science'},
            {'value': 'English', 'label': 'English'},
            {'value': 'Arts', 'label': 'Arts'},
        ]
    elif class_level in [8, 9, 10]:
        subjects = [
            {'value': 'Mathematics', 'label': 'Mathematics'},
            {'value': 'Physical Science', 'label': 'Physical Science'},
            {'value': 'Life Science', 'label': 'Life Science'},
            {'value': 'Arts', 'label': 'Arts'},
            {'value': 'English', 'label': 'English'},
        ]
    elif class_level in [11, 12]:
        subjects = [
            {'value': 'Mathematics', 'label': 'Mathematics'},
            {'value': 'Physics', 'label': 'Physics'},
            {'value': 'Biology', 'label': 'Biology'},
            {'value': 'Nutrition', 'label': 'Nutrition'},
            {'value': 'English', 'label': 'English'},
            {'value': 'Bengali', 'label': 'Bengali'},
        ]
    else:
        subjects = []
    
    return JsonResponse({'subjects': subjects})