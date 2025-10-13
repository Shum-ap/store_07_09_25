from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """
    Получение списка задач и создание новой.
    Фильтрация: status, deadline
    Поиск: title, description
    Сортировка: created_at
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление задачи.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SubTaskListCreateView(generics.ListCreateAPIView):
    """
    Получение списка подзадач и создание новой.
    Фильтрация: status, deadline
    Поиск: title, description
    Сортировка: created_at
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление подзадачи.
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer