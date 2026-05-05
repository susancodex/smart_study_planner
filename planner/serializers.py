from rest_framework import serializers
from .models import StudyPlan, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'study_plan', 'title', 'subject', 'priority', 'deadline', 'is_completed']
        read_only_fields = ['user']


class StudyPlanSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = StudyPlan
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'tasks']
        read_only_fields = ['user']

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and start > end:
            raise serializers.ValidationError({'end_date': 'End date must be after start date.'})
        return data
