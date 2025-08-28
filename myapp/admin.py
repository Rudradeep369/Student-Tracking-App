from django.contrib import admin
from myapp.models import Student,Batch,Teacher, Payment, Parent ,Achievement, StudyMaterial
from myapp.forms import BatchForm


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ['name', 'phone_number', 'board', 'student_class', 'subject', 'addmission_date', 'fees', 'total_due' ]
	search_fields = ['name', 'phone_number', 'board', 'student_class', 'subject']
	list_filter = ['board', 'student_class', 'subject']
	list_per_page = 10

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
	list_display = ['id','subject_name', 'batch_name', 'batch_times', 'batch_day', 'class_level', 'class_mode', 'start_date']
	search_fields = ['subject_name', 'batch_name', 'batch_times', 'batch_day', 'class_level', 'class_mode', 'start_date']
	list_filter = ['subject_name', 'batch_name', 'batch_times', 'batch_day', 'class_level', 'class_mode', 'start_date']
	list_per_page = 10
	# form = BatchForm

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
	list_display = ['name', 'phone_number', 'subject_teaches', 'qualification']
	search_fields = ['name', 'phone_number', 'subject_teaches', 'qualification']
	list_filter = ['name', 'phone_number', 'subject_teaches', 'qualification']
	list_per_page = 10

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ['student', 'amount', 'due_amount', 'date', 'months', 'modification']
	search_fields = ['student', 'amount', 'date']
	list_filter = ['student', 'amount', 'date']
	list_per_page = 10

# @admin.register(TotalDue)
# class TotalDueAdmin(admin.ModelAdmin):
# 	list_display = ['student', 'due']
# 	search_fields = ['student', 'due']
# 	list_filter = ['student', 'due']
# 	list_per_page = 10

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
	list_display = ['father_name', 'mother_name', 'father_phone_number', 'mother_phone_number', 'child']
	search_fields = ['father_name', 'mother_name', 'father_phone_number', 'mother_phone_number', 'child']
	list_filter = ['father_name', 'mother_name', 'father_phone_number', 'mother_phone_number', 'child']
	list_per_page = 10

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'class_name', 'score', 'board_name')
    search_fields = ('student_name', 'class_name', 'board_name')
    list_filter = ('class_name', 'board_name') 
    ordering = ('student_name',) 

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'class_level', 'subject', 'is_active', 'upload_date')
    list_filter = ('board', 'class_level', 'subject', 'is_active', 'upload_date')
    search_fields = ('title', 'description', 'board', 'subject')
    ordering = ('board', 'class_level', 'subject', 'title')
    list_per_page = 20
    readonly_fields = ('upload_date', 'last_updated')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Classification', {
            'fields': ('board', 'class_level', 'subject')
        }),
        ('Google Drive Link', {
            'fields': ('google_drive_link',)
        }),
        ('Timestamps', {
            'fields': ('upload_date', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view"""
        return super().get_queryset(request).select_related() 