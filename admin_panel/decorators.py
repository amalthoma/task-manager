from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import UserProfile


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            user_profile = request.user.userprofile
            if user_profile.role not in ['admin', 'superadmin']:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('admin_panel:dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('admin_panel:dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            user_profile = request.user.userprofile
            if user_profile.role != 'superadmin':
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('admin_panel:dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('admin_panel:dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
