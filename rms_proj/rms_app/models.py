from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Timestamp base model
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Status choices
class Status(models.TextChoices):
    PENDING = "Pending", "Pending"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"

# Request model
class Request(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    requirement = models.TextField()
    date = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    status_comment = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='status_updates')
    dummy_field = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.requirement[:20]} ({self.status})"

    def get_absolute_url(self):
        return reverse('request_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Request"
        verbose_name_plural = "Requests"
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['date']),
        ]



# Profile model for user metadata and role-based access
class Profile(models.Model):
    ROLE_CHOICES = (
        ('User', 'User'),
        ('Admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doj = models.DateField(auto_now_add=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    emp_id = models.CharField(max_length=20, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    pan = models.CharField(max_length=20, null=True, blank=True)
    salary_lpa = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    doj = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user.username} - {self.role or 'No Role'} ({self.emp_id or 'No ID'})"

# Settings model for dynamic key-value configuration
class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"

# Admin content model for dashboard or CMS blocks
class AdminModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
