from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubTaskViewSet, TaskByDayListView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/by-day/', TaskByDayListView.as_view(), name='task-by-day'),
]
