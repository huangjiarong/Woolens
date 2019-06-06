import django_filters

from .models import SaleOrder, Sale


class SaleOrderFilter(django_filters.rest_framework.FilterSet):
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    greater_remain = django_filters.NumberFilter(field_name='remain', lookup_expr='gt')
    woolens = django_filters.CharFilter(method='woolens_filter')
    client = django_filters.CharFilter(method='client_filter')

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(woolens__name=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(client__name=value)

    class Meta:
        model = SaleOrder
        fields = ['ord_num', 'greater_remain', 'woolens', 'client']


class SaleFilter(django_filters.rest_framework.FilterSet):
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    woolens = django_filters.CharFilter(method='woolens_filter')
    client = django_filters.CharFilter(method='client_filter')

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(woolens__name=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(client__name=value)

    class Meta:
        model = Sale
        fields = ['ord_num', 'woolens', 'client']
