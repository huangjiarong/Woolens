import django_filters

from .models import Reeling, ReelingReturn


class ReelingFilter(django_filters.rest_framework.FilterSet):
    """
    摇纱领料单的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    complete_return = django_filters.BooleanFilter(field_name='complete_return')
    woolens = django_filters.CharFilter(method='woolens_filter')
    client = django_filters.CharFilter(method='client_filter')

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(material__name=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(process__name=value)

    class Meta:
        model = Reeling
        fields = ['ord_num', 'complete_return', 'woolens', 'client', ]


class ReelingReturnFilter(django_filters.rest_framework.FilterSet):
    """
    购货订单的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')

    class Meta:
        model = ReelingReturn
        fields = ['ord_num',]


# class ReelingWarehouseFilter(django_filters.rest_framework.FilterSet):
#     """
#     原材料仓库的过滤类
#     """
#     greater_number = django_filters.NumberFilter(field_name='number', lookup_expr='gt')
#
#     class Meta:
#         model = ReelingWarehouse
#         fields = ['greater_number']
