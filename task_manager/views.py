from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime
from .models import SubTask, Task
from .serializers import SubTaskCreateSerializer, SubTaskSerializer, TaskDetailSerializer
from .pagination import SubTaskPagination

# Задание 1:
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

# Задание 2:
class SubTaskListCreateView(ListCreateAPIView):
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'task__title']
    pagination_class = SubTaskPagination

    def get_queryset(self):
        return SubTask.objects.all().order_by('-created_at')

# Задание 3:
class SubTaskFilteredList(ListAPIView):
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'task__title']
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all()
        queryset = queryset.order_by('-created_at')
        return queryset

class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer