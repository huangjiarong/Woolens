import django_filters

from .models import Packaging


class PackagingFilter(django_filters.rest_framework.FilterSet):
    """
    包装的过滤类
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Packaging
        fields = ['name', ]

