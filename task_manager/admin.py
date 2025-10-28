
from django.contrib import admin
from .models import Task, SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created_at')
    list_filter = ('status', 'owner')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'owner', 'status', 'created_at')
    list_filter = ('status', 'owner')
    search_fields = ('title',)
    ordering = ('-created_at',)