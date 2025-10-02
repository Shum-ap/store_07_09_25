from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

# --- Агрегирующий эндпойнт ---
class TaskByDayListView(ListAPIView):
    serializer_class = TaskSerializer

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
