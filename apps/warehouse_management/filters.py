import django_filters

from .models import Inventory, Transfers, Check


class InventoryFilter(django_filters.rest_framework.FilterSet):
    """
    库存的过滤类
    """
    greater_number = django_filters.NumberFilter(field_name='number', lookup_expr='gt')
    woolens_type = django_filters.CharFilter(field_name='woolens_type', lookup_expr='icontains')
    warehouse = django_filters.NumberFilter(method="warehouse_filter")
    warehouse_name = django_filters.CharFilter(method="warehousename_filter")

    def warehouse_filter(self, queryset, name, value):
        return queryset.filter(warehouse=value)

    def warehousename_filter(self, queryset, name, value):
        return queryset.filter(warehouse__name=value)

    class Meta:
        model = Inventory
        fields = ['greater_number', 'woolens_type', 'warehouse', 'warehouse_name', 'name']


class TransfersFilter(django_filters.rest_framework.FilterSet):
    """
    调拨单的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='contains')
    name = django_filters.CharFilter(method="name_filter")
    from_warehouse = django_filters.CharFilter(method="fromwarehouse_filter")
    to_warehouse = django_filters.CharFilter(method="towarehouse_filter")

    def name_filter(self, queryset, name, value):
        return queryset.filter(inventory__name=value)

    def fromwarehouse_filter(self, queryset, name, value):
        return queryset.filter(from_warehouse__name=value)

    def towarehouse_filter(self, queryset, name, value):
        return queryset.filter(to_warehouse__name=value)

    class Meta:
        model = Transfers
        fields = ['ord_num', 'name', 'to_warehouse', 'from_warehouse']


class CheckFilter(django_filters.rest_framework.FilterSet):
    """
    盘点的过滤类
    """
    ord_num = django_filters.CharFilter(field_name='ord_num', lookup_expr='contains')
    woolens = django_filters.CharFilter(method="woolens_filter")
    warehouse = django_filters.CharFilter(method="warehouse_filter")

    def woolens_filter(self, queryset, name, value):
        return queryset.filter(inventory__name=value)

    def warehouse_filter(self, queryset, name, value):
        return queryset.filter(warehouse__name=value)

    class Meta:
        model = Check
        fields = ['ord_num', 'woolens', 'warehouse']
