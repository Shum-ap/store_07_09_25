from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from store_8_09_25.pagination import SafeCursorPagination
from .models import Category, Task, SubTask
from .serializers import (
    CategorySerializer,
    TaskCreateSerializer,
    SubTaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    RegisterSerializer
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SafeCursorPagination

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = category.tasks.count()
        return Response({'category': category.name, 'task_count': count})

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SafeCursorPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['completed', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SafeCursorPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated]

class TaskByDayListView(ListAPIView):
    serializer_class = TaskDetailSerializer
    pagination_class = SafeCursorPagination

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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "Пользователь успешно зарегистрирован.",
            "user_id": user.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Неверные учетные данные."}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    response = Response({"message": "Успешный вход."}, status=status.HTTP_200_OK)
    response.set_cookie('refresh', str(refresh), httponly=True, secure=False)
    response.set_cookie('access', str(refresh.access_token), httponly=True, secure=False)
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass

    response = Response({"message": "Выход успешен."}, status=status.HTTP_205_RESET_CONTENT)
    response.delete_cookie('refresh')
    response.delete_cookie('access')
    return response