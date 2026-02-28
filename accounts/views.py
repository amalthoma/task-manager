from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

User = get_user_model()


def web_login(request):
    """Web login view for admin panel"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            django_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            # 'refresh': str(refresh),
            # 'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            # 'refresh': str(refresh),
            # 'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    try:
        # refresh_token = request.data["refresh"]
        # token = RefreshToken(refresh_token)
        # token.blacklist()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


def web_logout(request):
    """Web logout view for admin panel"""
    django_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
