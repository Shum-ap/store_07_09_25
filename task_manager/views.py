from rest_framework import generics, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task, SubTask
from rest_framework.views import APIView
from .serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskCreateSerializer,
    SubTaskSerializer,
)
from .permissions import IsOwnerOrReadOnly
User = get_user_model()

security = [{"Bearer": []}]


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_description="Создать новую задачу",
        request_body=TaskCreateSerializer,
        responses={201: TaskDetailSerializer, 400: "Неверные данные"},
        security=security
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить список задач текущего пользователя",
        responses={200: TaskDetailSerializer(many=True)},
        security=security
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()

    @swagger_auto_schema(
        operation_description="Получить детали задачи",
        responses={200: TaskDetailSerializer, 404: "Не найдено"},
        security=security
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить задачу (только владелец)",
        request_body=TaskCreateSerializer,
        responses={200: TaskDetailSerializer, 400: "Неверные данные", 403: "Запрещено"},
        security=security
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить задачу (только владелец)",
        request_body=TaskCreateSerializer,
        responses={200: TaskDetailSerializer, 400: "Неверные данные", 403: "Запрещено"},
        security=security
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить задачу (только владелец)",
        responses={204: "Успешно удалено", 403: "Запрещено", 404: "Не найдено"},
        security=security
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SubTaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SubTaskCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        if task.owner != self.request.user:
            from rest_framework.serializers import ValidationError
            raise ValidationError("Нельзя создавать подзадачи для чужих задач.")
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_description="Создать подзадачу",
        request_body=SubTaskCreateSerializer,
        responses={201: SubTaskSerializer, 400: "Неверные данные", 403: "Запрещено"},
        security=security
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Список подзадач текущего пользователя",
        responses={200: SubTaskSerializer(many=True)},
        security=security
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()

    @swagger_auto_schema(
        operation_description="Получить детали подзадачи",
        responses={200: SubTaskSerializer, 404: "Не найдено"},
        security=security
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить подзадачу (только владелец)",
        request_body=SubTaskCreateSerializer,
        responses={200: SubTaskSerializer, 400: "Неверные данные", 403: "Запрещено"},
        security=security
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить подзадачу (только владелец)",
        request_body=SubTaskCreateSerializer,
        responses={200: SubTaskSerializer, 400: "Неверные данные", 403: "Запрещено"},
        security=security
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить подзадачу (только владелец)",
        responses={204: "Успешно удалено", 403: "Запрещено", 404: "Не найдено"},
        security=security
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class TaskByDayListView(generics.ListAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        from django.utils.timezone import now
        today = now().date()
        return Task.objects.filter(owner=self.request.user, due_date=today)

    @swagger_auto_schema(
        operation_description="Получить задачи на сегодня",
        responses={200: TaskDetailSerializer(many=True)},
        security=security
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MyTasksListView(generics.ListAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    @swagger_auto_schema(
        operation_description="Получить все задачи текущего пользователя",
        responses={200: TaskDetailSerializer(many=True)},
        security=security
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        response = Response({'detail': 'Успешный вход'})
        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=60 * 60
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=7 * 24 * 60 * 60
        )
        return response


class LogoutView(views.APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = Response({'detail': 'Выход выполнен'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class RefreshTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token отсутствует'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'detail': 'Токен обновлён'})
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=60 * 60
            )
            return response
        except TokenError:
            return Response({'error': 'Неверный или просроченный refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not email or not password:
            return Response({'error': 'Email и пароль обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)


        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return Response({'detail': 'Регистрация успешна'}, status=status.HTTP_201_CREATED)