from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='assigned_tasks'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_tasks'
    )
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"
    
    def clean(self):
        if self.status == 'completed':
            if not self.completion_report:
                raise models.ValidationError({
                    'completion_report': 'Completion report is required when task is marked as completed.'
                })
            if self.worked_hours is None:
                raise models.ValidationError({
                    'worked_hours': 'Worked hours are required when task is marked as completed.'
                })
        else:
            self.completion_report = None
            self.worked_hours = None
