from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudyPlanViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'study-plans', StudyPlanViewSet, basename='study-plan')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]