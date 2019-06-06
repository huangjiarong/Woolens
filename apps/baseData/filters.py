import django_filters

from .models import Woolens, Warehouse, Client, Account, Staff


class WoolensFilter(django_filters.rest_framework.FilterSet):
    """
    毛料的过滤类
    """
    type = django_filters.CharFilter(method='type_filter')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    def type_filter(self, queryset, name, value):
        return queryset.filter(type__name=value)

    class Meta:
        model = Woolens
        fields = ['type', 'name', ]


class WarehouseFilter(django_filters.rest_framework.FilterSet):
    """
    仓库的过滤类
    """
    type = django_filters.CharFilter(method='type_filter')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    def type_filter(self, queryset, name, value):
        return queryset.filter(type__name__contains=value)

    class Meta:
        model = Warehouse
        fields = ['type', 'name', ]


class ClientFilter(django_filters.rest_framework.FilterSet):
    """
    客户的过滤类
    """
    clientType_name = django_filters.CharFilter(method='clientType_filter')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    def clientType_filter(self, queryset, name, value):
        return queryset.filter(type__name=value)

    class Meta:
        model = Client
        fields = ['clientType_name', 'name', ]


class AccountFilter(django_filters.rest_framework.FilterSet):
    """
    账户的过滤类
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Account
        fields = ['name', ]


class StaffFilter(django_filters.rest_framework.FilterSet):
    number = django_filters.CharFilter(field_name='number', lookup_expr='icontains')

    class Meta:
        model = Staff
        fields = ['number', ]
