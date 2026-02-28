from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile
from tasks.models import Task


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=False)
    role = forms.ChoiceField(choices=[
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'SuperAdmin'),
    ], initial='user')
    assigned_admin = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__role__in=['admin', 'superadmin']),
        required=False,
        empty_label="None"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If we have an existing user instance, populate the profile fields
        if self.instance and self.instance.pk:
            try:
                profile = self.instance.userprofile
                self.fields['role'].initial = profile.role
                self.fields['assigned_admin'].initial = profile.assigned_admin
            except UserProfile.DoesNotExist:
                pass
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            raise forms.ValidationError("Passwords don't match.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
            
            # Update or create UserProfile
            role = self.cleaned_data.get('role', 'user')
            assigned_admin = self.cleaned_data.get('assigned_admin')
            
            try:
                profile = user.userprofile
                profile.role = role
                profile.assigned_admin = assigned_admin
                profile.save()
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(
                    user=user,
                    role=role,
                    assigned_admin=assigned_admin
                )
        
        return user


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'completion_report': forms.Textarea(attrs={'rows': 4}),
            'worked_hours': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user
        
        if user:
            if user.is_superuser:
                self.fields['assigned_to'].queryset = User.objects.all()
            else:
                self.fields['assigned_to'].queryset = User.objects.all()
    
    def save(self, commit=True):
        task = super().save(commit=False)
        if self.user:
            task.created_by = self.user
        
        if commit:
            task.save()
        
        return task
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        completion_report = cleaned_data.get('completion_report')
        worked_hours = cleaned_data.get('worked_hours')
        
        if status == 'completed':
            if not completion_report:
                raise forms.ValidationError({
                    'completion_report': 'Completion report is required when task is marked as completed.'
                })
            if worked_hours is None:
                raise forms.ValidationError({
                    'worked_hours': 'Worked hours are required when task is marked as completed.'
                })
        
        return cleaned_data


class UserAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select User"
    )
    admin = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Assign to Admin"
    )
