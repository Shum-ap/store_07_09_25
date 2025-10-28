from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    TaskByDayListView,
    MyTasksListView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    RegisterView,
)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # задачи
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),

    # подзадачи
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'),

    # агрегирующий эндпоинт
    path('tasks/by-day/', TaskByDayListView.as_view(), name='task-by-day'),

    # задачи текущего пользователя
    path('my-tasks/', MyTasksListView.as_view(), name='my-tasks-list'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]