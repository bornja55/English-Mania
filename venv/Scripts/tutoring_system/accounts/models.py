# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('CEO', 'CEO'),
        ('CTO', 'CTO'),
        ('ADMIN', 'Admin Officer'),
        ('TUTOR', 'Tutor'),
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    line_id = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    additional_info = models.JSONField(default=dict, blank=True)  # For future extensibility

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_hours = models.JSONField(default=dict)
    specializations = models.JSONField(default=list)  # Store tutor specializations
    additional_info = models.JSONField(default=dict, blank=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='children')
    grade = models.CharField(max_length=20)
    learning_style = models.CharField(max_length=50, blank=True)  # For personalized learning
    additional_info = models.JSONField(default=dict, blank=True)

# courses/models.py
class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        ('HOURLY', 'Hourly'),
        ('MONTHLY', 'Monthly'),
        ('TERM', 'Term'),
    )
    name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    grade = models.CharField(max_length=20)
    description = models.TextField()
    tutors = models.ManyToManyField(Tutor, related_name='courses')
    max_students = models.IntegerField(default=1)  # For group classes
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    materials = models.JSONField(default=list)  # Store course materials
    additional_info = models.JSONField(default=dict, blank=True)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Active')
    progress = models.JSONField(default=dict)  # Track student progress
    additional_info = models.JSONField(default=dict, blank=True)

# scheduling/models.py
class Schedule(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, default='Scheduled')
    location = models.CharField(max_length=100, default='Online')  # For hybrid learning
    attendance = models.JSONField(default=dict)  # Track attendance
    additional_info = models.JSONField(default=dict, blank=True)

# billing/models.py
class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(auto_now_add=True)
    date_paid = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Unpaid')
    payment_method = models.CharField(max_length=50, blank=True)
    items = models.JSONField(default=list)  # Detailed invoice items
    additional_info = models.JSONField(default=dict, blank=True)

class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=20)
    comments = models.TextField()
    date = models.DateField(auto_now_add=True)
    skills_assessment = models.JSONField(default=dict)  # Detailed skills assessment
    additional_info = models.JSONField(default=dict, blank=True)