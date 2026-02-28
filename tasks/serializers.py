from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_username',
            'created_by', 'created_by_username', 'due_date', 'status',
            'completion_report', 'worked_hours', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': 'Completion report is required when task is marked as completed.'
                })
            if data.get('worked_hours') is None:
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours are required when task is marked as completed.'
                })
        return data
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
    
    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': 'Completion report is required when task is marked as completed.'
                })
            if data.get('worked_hours') is None:
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours are required when task is marked as completed.'
                })
        return data


class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_username',
            'created_by', 'created_by_username', 'due_date', 'status',
            'completion_report', 'worked_hours', 'created_at', 'updated_at'
        ]
        read_only_fields = '__all__'
