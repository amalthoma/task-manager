from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from tasks.models import Task
from accounts.models import UserProfile
from .forms import UserForm, TaskForm, UserAssignmentForm
from .decorators import admin_required, superadmin_required

User = get_user_model()


@login_required
def dashboard(request):
    try:
        user_profile = request.user.userprofile
        user_role = user_profile.role
    except UserProfile.DoesNotExist:
        # Create a default profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user, role='user')
        user_role = 'user'
    
    if user_role == 'superadmin':
        total_users = UserProfile.objects.filter(role='user').count()
        total_admins = UserProfile.objects.filter(role='admin').count()
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='completed').count()
        
        context = {
            'total_users': total_users,
            'total_admins': total_admins,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'recent_tasks': Task.objects.all()[:10],
        }
        
    elif user_role == 'admin':
        assigned_users = User.objects.filter(userprofile__assigned_admin=request.user)
        total_users = assigned_users.count()
        total_tasks = Task.objects.filter(assigned_to__in=assigned_users).count()
        completed_tasks = Task.objects.filter(
            assigned_to__in=assigned_users, 
            status='completed'
        ).count()
        
        context = {
            'total_users': total_users,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'recent_tasks': Task.objects.filter(assigned_to__in=assigned_users)[:10],
            'assigned_users': assigned_users,
        }
        
    else:
        total_tasks = Task.objects.filter(assigned_to=request.user).count()
        completed_tasks = Task.objects.filter(assigned_to=request.user, status='completed').count()
        
        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'recent_tasks': Task.objects.filter(assigned_to=request.user)[:10],
        }
    
    return render(request, 'admin_panel/dashboard.html', context)


@superadmin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_panel/user_list.html', {'users': users})


@superadmin_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('admin_panel:user_list')
    else:
        form = UserForm()
    
    return render(request, 'admin_panel/user_form.html', {'form': form, 'title': 'Create User'})


@superadmin_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully.')
            return redirect('admin_panel:user_list')
    else:
        form = UserForm(instance=user)
    
    return render(request, 'admin_panel/user_form.html', {'form': form, 'title': 'Update User'})


@superadmin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully.')
        return redirect('admin_panel:user_list')
    
    return render(request, 'admin_panel/user_confirm_delete.html', {'user': user})


@superadmin_required
def admin_list(request):
    admins = User.objects.filter(userprofile__role__in=['admin', 'superadmin'])
    return render(request, 'admin_panel/admin_list.html', {'admins': admins})


@superadmin_required
def admin_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            admin = form.save()
            messages.success(request, f'Admin {admin.username} created successfully.')
            return redirect('admin_panel:admin_list')
    else:
        form = UserForm()
    
    return render(request, 'admin_panel/admin_form.html', {'form': form, 'title': 'Create Admin'})


@superadmin_required
def admin_update(request, pk):
    admin = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, f'Admin {admin.username} updated successfully.')
            return redirect('admin_panel:admin_list')
    else:
        form = UserForm(instance=admin)
    
    return render(request, 'admin_panel/admin_form.html', {'form': form, 'title': 'Update Admin'})


@superadmin_required
def admin_delete(request, pk):
    admin = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = admin.username
        admin.delete()
        messages.success(request, f'Admin {username} deleted successfully.')
        return redirect('admin_panel:admin_list')
    
    return render(request, 'admin_panel/admin_confirm_delete.html', {'admin': admin})


@login_required
def task_list(request):
    try:
        user_profile = request.user.userprofile
        user_role = user_profile.role
    except UserProfile.DoesNotExist:
        user_role = 'user'
    
    if user_role == 'superadmin':
        tasks = Task.objects.all()
    elif user_role == 'admin':
        assigned_users = User.objects.filter(userprofile__assigned_admin=request.user)
        tasks = Task.objects.filter(
            Q(assigned_to__in=assigned_users) | Q(assigned_to=request.user)
        )
    else:
        tasks = Task.objects.filter(assigned_to=request.user)
    
    return render(request, 'admin_panel/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    try:
        user_profile = request.user.userprofile
        user_role = user_profile.role
    except UserProfile.DoesNotExist:
        user_role = 'user'
    
    if user_role == 'user':
        messages.error(request, 'You do not have permission to create tasks.')
        return redirect('admin_panel:task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" created successfully.')
            return redirect('admin_panel:task_list')
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'admin_panel/task_form.html', {'form': form, 'title': 'Create Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    try:
        user_profile = request.user.userprofile
        user_role = user_profile.role
    except UserProfile.DoesNotExist:
        user_role = 'user'
    
    if user_role == 'user' and task.assigned_to != request.user:
        messages.error(request, 'You can only update your own tasks.')
        return redirect('admin_panel:task_list')
    
    if user_role == 'admin':
        try:
            task_assigned_admin = task.assigned_to.userprofile.assigned_admin
            if task_assigned_admin != request.user and task.assigned_to != request.user:
                messages.error(request, 'You can only update tasks assigned to your users.')
                return redirect('admin_panel:task_list')
        except UserProfile.DoesNotExist:
            if task.assigned_to != request.user:
                messages.error(request, 'You can only update tasks assigned to your users.')
                return redirect('admin_panel:task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" updated successfully.')
            return redirect('admin_panel:task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    
    return render(request, 'admin_panel/task_form.html', {'form': form, 'title': 'Update Task'})


@login_required
def task_report(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if task.status != 'completed':
        messages.error(request, 'Report is only available for completed tasks.')
        return redirect('admin_panel:task_list')
    
    try:
        user_profile = request.user.userprofile
        user_role = user_profile.role
    except UserProfile.DoesNotExist:
        user_role = 'user'
    
    if user_role == 'user' and task.assigned_to != request.user:
        messages.error(request, 'You can only view reports for your own tasks.')
        return redirect('admin_panel:task_list')
    
    if user_role == 'admin':
        try:
            task_assigned_admin = task.assigned_to.userprofile.assigned_admin
            if task_assigned_admin != request.user and task.assigned_to != request.user:
                messages.error(request, 'You can only view reports for your users.')
                return redirect('admin_panel:task_list')
        except UserProfile.DoesNotExist:
            if task.assigned_to != request.user:
                messages.error(request, 'You can only view reports for your users.')
                return redirect('admin_panel:task_list')
    
    return render(request, 'admin_panel/task_report.html', {'task': task})


@superadmin_required
def assign_user_to_admin(request):
    if request.method == 'POST':
        form = UserAssignmentForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            admin = form.cleaned_data['admin']
            user.assigned_admin = admin
            user.save()
            messages.success(request, f'User {user.username} assigned to admin {admin.username}.')
            return redirect('admin_panel:user_list')
    else:
        form = UserAssignmentForm()
    
    return render(request, 'admin_panel/assign_user.html', {'form': form})
