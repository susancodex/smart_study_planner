from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import StudyPlan, Task
from .serializers import StudyPlanSerializer, TaskSerializer


class IsOwner(permissions.BasePermission):
    """Only allow users to access their own objects."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


@extend_schema_view(
    list=extend_schema(tags=['Study Plans'], operation_id='study_plans_list', summary='List my study plans'),
    retrieve=extend_schema(tags=['Study Plans'], operation_id='study_plans_retrieve', summary='Get a study plan'),
    create=extend_schema(tags=['Study Plans'], operation_id='study_plans_create', summary='Create a study plan'),
    update=extend_schema(tags=['Study Plans'], operation_id='study_plans_update', summary='Update a study plan'),
    partial_update=extend_schema(tags=['Study Plans'], operation_id='study_plans_partial_update', summary='Partially update a study plan'),
    destroy=extend_schema(tags=['Study Plans'], operation_id='study_plans_destroy', summary='Delete a study plan'),
)
class StudyPlanViewSet(viewsets.ModelViewSet):
    """CRUD for study plans. Each user only sees their own plans."""

    serializer_class = StudyPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return StudyPlan.objects.none()
        return StudyPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(tags=['Study Plans'], operation_id='study_plan_progress', summary='Get completion percentage')
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Returns the percentage of completed tasks in this study plan."""
        plan = self.get_object()
        total = plan.tasks.count()
        if total == 0:
            return Response({'completion_percentage': 0.0})
        completed = plan.tasks.filter(is_completed=True).count()
        return Response({'completion_percentage': round(completed / total * 100, 2)})


@extend_schema_view(
    list=extend_schema(tags=['Tasks'], operation_id='tasks_list', summary='List my tasks'),
    retrieve=extend_schema(tags=['Tasks'], operation_id='tasks_retrieve', summary='Get a task'),
    create=extend_schema(tags=['Tasks'], operation_id='tasks_create', summary='Create a task'),
    update=extend_schema(tags=['Tasks'], operation_id='tasks_update', summary='Update a task'),
    partial_update=extend_schema(tags=['Tasks'], operation_id='tasks_partial_update', summary='Partially update a task'),
    destroy=extend_schema(tags=['Tasks'], operation_id='tasks_destroy', summary='Delete a task'),
)
class TaskViewSet(viewsets.ModelViewSet):
    """CRUD for tasks. Supports filtering by subject, priority, and completion status."""

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
