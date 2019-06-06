import django_filters

from .models import Hairing, HairingReturn


class HairingFilter(django_filters.rest_framework.FilterSet):
    """
    打毛领料的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    greater_remain = django_filters.NumberFilter(field_name='remain', lookup_expr='gt')
    complete_return = django_filters.BooleanFilter(field_name='complete_return')
    woolens = django_filters.CharFilter(method='woolens_filter')
    client = django_filters.CharFilter(method='client_filter')

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(dye_goods__name=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(process__name=value)

    class Meta:
        model = Hairing
        fields = ['ord_num', 'greater_remain', 'complete_return', 'client', 'woolens']


class HairingReturnFilter(django_filters.rest_framework.FilterSet):
    """
    打毛领料的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')

    class Meta:
        model = HairingReturn
        fields = ['ord_num', ]
