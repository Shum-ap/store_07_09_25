from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyView.as_view(), name='task-detail-update-delete'),

    path('subtasks/', views.SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', views.SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail-update-delete'),

    path('tasks/by-day/', views.TaskByDayListView.as_view(), name='task-by-day'),

    path('subtasks/filter/', views.SubTaskFilteredList.as_view(), name='subtask-filtered-list'),
]