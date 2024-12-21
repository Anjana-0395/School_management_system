from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('librarian', 'Librarian'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    def save(self, *args, **kwargs):
        # Automatically set role to 'admin' if the user is a superuser
        if self.is_superuser:
            self.role = 'admin'
        super(User, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    
    class Meta:
        # Adding related_name to avoid conflicts with default User model
        permissions = [
            # ("can_manage_students", "Can manage students"),
            # ("can_manage_library_books", "Can manage library books"),
            # ("can_view_library_books", "Can view library books"),
        ]
    
    # Overriding the fields to add related_name
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='custom_user_groups', 
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='custom_user_permissions', 
        blank=True
    )

        
class Student(models.Model):
    CLASS_CHOICES = [
        ('I', 'Class I'),
        ('II', 'Class II'),
        ('III', 'Class III'),
        ('IV', 'Class IV'),
        ('V', 'Class V'),
        ('VI', 'Class VI'),
        ('VII', 'Class VII'),
        ('VIII', 'Class VIII'),
        ('IX', 'Class IX'),
        ('X', 'Class X'),
    ]
    DIVISION_CHOICES = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
    ]
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    class_name = models.CharField(max_length=5, choices=CLASS_CHOICES)
    division = models.CharField(max_length=5, choices=DIVISION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}"


class Staff(models.Model):
    DEPARTMENT_CHOICES = [
        ('LP','Lower Primary'),
        ('UP','Upper Primary'),
        ('HS','High School'),
        
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    staff_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100,choices=DEPARTMENT_CHOICES)
    joining_date = models.DateField()

    def __str__(self):
        return f"Staff: {self.user.username} - {self.department}"

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="librarian_profile")
    librarian_name = models.CharField(max_length=100)
    joining_date = models.DateField()
    library_section = models.CharField(max_length=100)

    def __str__(self):
        return f"Librarian: {self.user.username}"

class LibraryHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=150)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('borrowed','Borrowed'), ('returned','Returned')])
    
    def clean(self):
        # Validate return_date is not before borrow_date
        if self.return_date and self.return_date < self.borrow_date:
            raise ValidationError(_('Return date cannot be earlier than borrow date.'))

        # Validate return_date is required if status is 'returned'
        if self.status == 'returned' and not self.return_date:
            raise ValidationError(_('Return date is required when status is "returned".'))
    def __str__(self):
        return f"{self.book_name} ({self.status}) - {self.student.full_name}"
    

class FeeHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=100) # tuition fee, sem fee, bus etc
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.fee_type} - {self.amount} ({self.student.full_name})"
