import django_filters

from .models import PurchaseOrder, TakeGoods, Purchase


class PurchaseOrderFilter(django_filters.rest_framework.FilterSet):
    """
    购货订单的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    woolens = django_filters.CharFilter(method='woolens_filter')
    client = django_filters.CharFilter(method='client_filter')
    remain = django_filters.NumberFilter(field_name='remain', lookup_expr='gt')
    complete_return = django_filters.BooleanFilter(field_name='complete_return')

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(woolens__name=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(supplier__name=value)

    class Meta:
        model = PurchaseOrder
        fields = ['ord_num', 'remain', 'complete_return', 'woolens', 'client']


class PurchaseFilter(django_filters.rest_framework.FilterSet):
    """
    购货单的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')
    woolens = django_filters.CharFilter(method='woolens_filter')
    client = django_filters.CharFilter(method='client_filter')

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(woolens__name=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(supplier__name=value)

    class Meta:
        model = Purchase
        fields = ['ord_num', 'woolens', 'client']


class TakeGoodsFilter(django_filters.rest_framework.FilterSet):
    """
    取货表的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='exact')

    class Meta:
        model = TakeGoods
        fields = ['ord_num']


