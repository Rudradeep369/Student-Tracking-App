from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    phone_number2 = models.CharField(max_length=15, blank=True)
    board = models.CharField(max_length=50, choices=[('CBSE', 'CBSE'), ('WBBSE', 'WBBSE'), ('ICSE', 'ICSE')])
    student_class = models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])
    subject = models.CharField(max_length=100, default='All')
    addmission_date = models.DateField(default=timezone.now)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
    @property
    def total_due(self):
        payments = self.payments.all()
        total_due = sum(payment.due_amount for payment in payments)
        return total_due

class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    father_phone_number = models.CharField(max_length=15, blank=True)
    mother_phone_number = models.CharField(max_length=15, blank=True)
    child = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents', default=None)

    def __str__(self):
        return f"{self.father_name} - {self.mother_name} - {self.child.name}"

class Payment(models.Model):
    MONTH_CHOICES = [
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method= models.CharField(max_length=100, choices=[('CASH', 'CASH'), ('UPI', 'UPI'), ('CARD', 'CARD')], default='CASH')
    date = models.DateField(default=timezone.now)
    months = MultiSelectField(choices=MONTH_CHOICES, default='1', max_length=100)
    modification  = models.CharField(blank=True, null=True, default="", max_length=50)

    def __str__(self):
        return f"{self.student.name} - {self.amount} - {self.months}"
    

class Teacher(models.Model):
    profile_image=models.ImageField(null=True,blank=True,upload_to="teacher-img/")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    subject_teaches = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name
    
class Batch(models.Model):
    DAYS = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    subject_name = models.CharField(max_length=100)
    batch_name = models.CharField(max_length=100, default="")
    batch_times = models.JSONField(default=dict)  # Store time for each day as a JSON object
    batch_day = MultiSelectField(choices=DAYS,default=["MON"])
    class_level = models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])
    class_mode = models.CharField(max_length=100, choices=[('ONLINE', 'ONLINE'), ('OFFLINE', 'OFFLINE')], default='ONLINE')  
    start_date = models.DateField(default=timezone.now) 
    teachers = models.ManyToManyField(Teacher, related_name='teachers')
    students = models.ManyToManyField(Student, related_name='students', blank=True)

    def __str__(self):
        return f"{self.subject_name} - {self.batch_day}"

    def get_batch_time(self, day):
        return self.batch_times.get(day, "Not scheduled")


class Achievement(models.Model):
    student_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    board_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='achievement-img/')

    def __str__(self):
        return self.student_name


# Signal handlers for automatic media file deletion
@receiver(post_delete, sender=Teacher)
def delete_teacher_image_on_delete(sender, instance, **kwargs):
    """Delete teacher image file when Teacher instance is deleted."""
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)


@receiver(post_delete, sender=Achievement)
def delete_achievement_image_on_delete(sender, instance, **kwargs):
    """Delete achievement image file when Achievement instance is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Teacher)
def delete_teacher_image_on_change(sender, instance, **kwargs):
    """Delete old teacher image file when Teacher image is updated."""
    if not instance.pk:
        return False

    try:
        old_file = Teacher.objects.get(pk=instance.pk).profile_image
    except Teacher.DoesNotExist:
        return False

    new_file = instance.profile_image
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(pre_save, sender=Achievement)
def delete_achievement_image_on_change(sender, instance, **kwargs):
    """Delete old achievement image file when Achievement image is updated."""
    if not instance.pk:
        return False

    try:
        old_file = Achievement.objects.get(pk=instance.pk).image
    except Achievement.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)