import django_filters

from .models import Dye, DyeNotice, DyeReturn


class DyeFilter(django_filters.rest_framework.FilterSet):
    """
    染色领料的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    greater_remain = django_filters.NumberFilter(field_name='remain', lookup_expr='gt')
    complete_return = django_filters.BooleanFilter(field_name='complete_return')
    woolens = django_filters.CharFilter(method='woolens_filter')
    client = django_filters.CharFilter(method='client_filter')

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(reeling__name=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(process__name=value)

    class Meta:
        model = Dye
        fields = ['ord_num', 'greater_remain', 'complete_return', 'woolens', 'client']


class DyeNoticeFilter(django_filters.rest_framework.FilterSet):
    """
    染色领料的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    complete_return = django_filters.BooleanFilter(field_name='complete_return')

    class Meta:
        model = DyeNotice
        fields = ['ord_num', 'complete_return']


class DyeReturnFilter(django_filters.rest_framework.FilterSet):
    """
    染色回毛的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')

    class Meta:
        model = DyeReturn
        fields = ['ord_num',]

