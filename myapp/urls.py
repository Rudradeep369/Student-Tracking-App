from django.contrib.auth import views as auth_views
from django.urls import path
from myapp import views
from .views import create_batch, view_batches, BatchDetailView, add_existing_students, add_new_student,edit_teacher, delete_teacher

urlpatterns = [
    path('index/', views.index, name='index'),
    # path('edit/<int:student_id>/', views.edit_student, name='edit_student'),  # Uncomment if needed
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
	path('filter-student/', views.filter_students, name='filter_student'),
    path('all-students/', views.all_students, name='all_students'),
    path('add-student/', views.add_student, name='add_student'),
    path('create-batch/', create_batch, name='create_batch'),
    path('view-batches/', view_batches, name='view_batches'),
    path('batch/<int:pk>/', BatchDetailView.as_view(), name='batch_detail'),
    path('batch/<int:pk>/add-existing-students/', add_existing_students, name='add_existing_students'),
    path('batch/<int:pk>/add-new-student/', add_new_student, name='add_new_student'),
    path('batch/<int:pk>/assign-teachers/', views.assign_teacher_to_batch, name='assign_teacher_to_batch'),
    path('batch/<int:pk>/remove-teacher/<int:teacher_id>/', views.remove_teacher_from_batch, name='remove_teacher_from_batch'),
    path('edit-batch/<int:id>/', views.edit_batch, name='edit_batch'),
    # Ensure there's also a delete_batch path
    path('delete-batch/<int:id>/', views.delete_batch, name='delete_batch'),
    path('batch/<int:batch_id>/remove_student/<int:student_id>/', views.remove_student_from_batch, name='remove_student_from_batch'),

    path('student/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),

    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('all-teachers/', views.all_teachers, name='all_teachers'),
    path('teacher/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),

    path('edit_teacher/<int:teacher_id>/', edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
	

    path('add-payment/<int:student_id>', views.payment_record, name='payment_record'),
	path('all-payments/', views.all_payment, name='all_payments'),
	
	path('update-payment/<int:id>/<int:std_id>/', views.edit_payment, name='update_payment'),

    path('add-parent/<int:std_id>/',views.add_parent, name="add_parent"),
    path('edit-parent/<int:id>/<int:std_id>/',views.edit_parent, name="edit_parent"),
	


    path('accounts/login/', views.user_login, name='login'),    
    path('accounts/logout/', views.user_logout, name='logout'),
	

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('',views.home, name="home"),
    path('class_details/',views.class_details, name="class_details"),
    
    path('achievement/', views.achievement, name='achievement'),
    path('edit_achievement/<int:achievement_id>/', views.edit_achievement, name='edit_achievement'),
    path('delete_achievement/<int:achievement_id>/', views.delete_achievement, name='delete_achievement'),

    # Study Material URLs
    path('add-study-material/', views.add_study_material, name='add_study_material'),
    path('all-study-materials/', views.all_study_materials, name='all_study_materials'),
    path('study-materials/<int:class_level>/<str:subject>/<str:board>/', views.study_materials_by_filter, name='study_materials_by_filter'),
    path('ajax/get-subjects/', views.get_subjects_for_class, name='get_subjects_for_class'),

]


