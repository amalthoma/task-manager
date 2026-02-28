from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'SuperAdmin'),
    ]
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    assigned_admin = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_users',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role in ['admin', 'superadmin']
    
    @property
    def is_superadmin(self):
        return self.role == 'superadmin'
