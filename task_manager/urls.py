from django.urls import path
from . import views

urlpatterns = [
    path('subtasks/', views.SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', views.SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('tasks/by-day/', views.TaskByDayListView.as_view(), name='task-by-day'),
    path('subtasks/filter/', views.SubTaskFilteredList.as_view(), name='subtask-filtered-list'),
]