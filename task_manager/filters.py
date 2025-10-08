import django_filters
from .models import SubTask

class SubTaskFilter(django_filters.FilterSet):
    task_title = django_filters.CharFilter(
        field_name='task__title',
        lookup_expr='icontains'
    )

    class Meta:
        model = SubTask
        fields = ['completed']