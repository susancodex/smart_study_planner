from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import StudyPlan, Task
from .serializers import StudyPlanSerializer, TaskSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

@extend_schema_view(
    list=extend_schema(tags=['Study Plans'], operation_id='study_plans_list', summary='List study plans'),
    retrieve=extend_schema(tags=['Study Plans'], operation_id='study_plans_retrieve', summary='Get a study plan'),
    create=extend_schema(tags=['Study Plans'], operation_id='study_plans_create', summary='Create a study plan'),
    update=extend_schema(tags=['Study Plans'], operation_id='study_plans_update', summary='Update a study plan'),
    partial_update=extend_schema(tags=['Study Plans'], operation_id='study_plans_partial_update', summary='Partially update a study plan'),
    destroy=extend_schema(tags=['Study Plans'], operation_id='study_plans_destroy', summary='Delete a study plan'),
)
class StudyPlanViewSet(viewsets.ModelViewSet):
    serializer_class = StudyPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return StudyPlan.objects.none()
        return StudyPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(tags=['Study Plans'], operation_id='study_plan_progress', summary='Get study plan progress')
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        study_plan = self.get_object()
        total_tasks = study_plan.tasks.count()
        if total_tasks == 0:
            return Response({"completion_percentage": 0.0})
        completed_tasks = study_plan.tasks.filter(is_completed=True).count()
        percentage = (completed_tasks / total_tasks) * 100
        return Response({"completion_percentage": round(percentage, 2)})

@extend_schema_view(
    list=extend_schema(tags=['Tasks'], operation_id='tasks_list', summary='List tasks'),
    retrieve=extend_schema(tags=['Tasks'], operation_id='tasks_retrieve', summary='Get a task'),
    create=extend_schema(tags=['Tasks'], operation_id='tasks_create', summary='Create a task'),
    update=extend_schema(tags=['Tasks'], operation_id='tasks_update', summary='Update a task'),
    partial_update=extend_schema(tags=['Tasks'], operation_id='tasks_partial_update', summary='Partially update a task'),
    destroy=extend_schema(tags=['Tasks'], operation_id='tasks_destroy', summary='Delete a task'),
)
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['subject', 'is_completed', 'priority']
    search_fields = ['title', 'subject']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)