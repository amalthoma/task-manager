from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_list(request):
    user = request.user
    if user.role == 'superadmin':
        tasks = Task.objects.all()
    elif user.role == 'admin':
        tasks = Task.objects.filter(assigned_to__assigned_admin=user) | Task.objects.filter(assigned_to=user)
    else:
        tasks = Task.objects.filter(assigned_to=user)
    
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.user.role == 'user' and task.assigned_to != request.user:
        return Response(
            {'error': 'You can only update your own tasks'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.user.role == 'admin' and task.assigned_to.assigned_admin != request.user:
        return Response(
            {'error': 'You can only update tasks assigned to your users'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        updated_task = serializer.save()
        return Response(TaskSerializer(updated_task).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_report(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if task.status != 'completed':
        return Response(
            {'error': 'Report is only available for completed tasks'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = request.user
    if user.role == 'user':
        if task.assigned_to != user:
            return Response(
                {'error': 'You can only view reports for your own tasks'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    elif user.role == 'admin':
        if task.assigned_to.assigned_admin != user and task.assigned_to != user:
            return Response(
                {'error': 'You can only view reports for your users'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = TaskReportSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_task(request):
    user = request.user
    
    if user.role == 'user':
        return Response(
            {'error': 'Users cannot create tasks'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = TaskSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        task = serializer.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
