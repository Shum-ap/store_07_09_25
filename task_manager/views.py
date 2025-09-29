from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import SubTask, Task, Category
from .serializers import (
    TaskCreateSerializer,
    SubTaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    CategorySerializer
)


# Задание 1:
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        task_count = Task.objects.filter(category=category, is_deleted=False).count()
        return Response({'task_count': task_count})

# Задание 2:
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['completed', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

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

class SubTaskFilteredList(ListAPIView):
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'task__title']


    def get_queryset(self):
        queryset = SubTask.objects.all()
        queryset = queryset.order_by('-created_at')
        return queryset