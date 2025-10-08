from django.db import models
from django.utils import timezone


# --- Менеджер для мягкого удаления ---
class CategoryManager(models.Manager):
    def get_queryset(self):
        # Показываем только не удалённые категории
        return super().get_queryset().filter(is_deleted=False)


# --- Категории ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # для мягкого удаления
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CategoryManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name


# --- Задачи ---
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    deadline = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # статус задачи

    def __str__(self):
        return self.title


# --- Подзадачи ---
class SubTask(models.Model):
    title = models.CharField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    completed = models.BooleanField(default=False)  # статус
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
