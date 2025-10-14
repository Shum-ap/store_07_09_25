from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .models import Category, Task, SubTask
from .serializers import (
    CategorySerializer,
    TaskCreateSerializer,
    SubTaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer
)
from .permissions import IsOwnerOrReadOnly 


#  Category CRUD + мягкое удаление

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        """Подсчёт количества задач в категории"""
        category = self.get_object()
        count = category.tasks.count()
        return Response({'category': category.name, 'task_count': count})

    def perform_destroy(self, instance):
        """Переопределяем удаление для мягкого удаления"""
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()


#  Tasks CRUD — Generic Views

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['completed', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



#  SubTasks CRUD — Generic Views

class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer): 
        serializer.save(owner=self.request.user)


class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



#  Aggregating endpoint
class TaskByDayListView(ListAPIView):
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        day = self.request.query_params.get('day', None)
        if day:
            days_map = {
                'monday': 1,
                'tuesday': 2,
                'wednesday': 3,
                'thursday': 4,
                'friday': 5,
                'saturday': 6,
                'sunday': 7
            }
            day_num = days_map.get(day.lower(), None)
            if day_num:
                return Task.objects.filter(due_date__week_day=day_num)
        return Task.objects.all()



#  Задание 1: Получение задач текущего пользователя

class MyTasksListView(ListAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self, 'request'):
            return Task.objects.filter(owner=self.request.user)
        return Task.objects.none()
