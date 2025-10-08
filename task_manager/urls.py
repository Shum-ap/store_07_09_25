from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    TaskByDayListView,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),

    # --- задачи ---
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),

    # --- подзадачи ---
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'),

    # --- агрегирующий эндпойнт ---
    path('tasks/by-day/', TaskByDayListView.as_view(), name='task-by-day'),
]
