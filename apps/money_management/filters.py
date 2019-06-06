import django_filters

from baseData.models import Client
from .models import Due, Account_Due, Receipt, Payment


class DueFilters(django_filters.rest_framework.FilterSet):
    """
    应付款的过滤类
    """
    client = django_filters.NumberFilter(method='client_filters')
    #该字段过滤出未核销大于某个数的数据
    greater_not_cancel = django_filters.NumberFilter(field_name='not_cancel', lookup_expr='gt')

    def client_filters(self, queryset, name, value):
        #过滤出该客户的所有应付款
        return queryset.filter(client=value)

    class Meta:
        model = Due
        fields = ['client', 'greater_not_cancel']


class AccountDueFilters(django_filters.rest_framework.FilterSet):
    """
    应收款的过滤类
    """
    client = django_filters.NumberFilter(method='client_filters')
    #该字段过滤出未核销大于某个数的数据
    greater_not_cancel = django_filters.NumberFilter(field_name='not_cancel', lookup_expr='gt')

    def client_filters(self, queryset, name, value):
        #过滤出该客户的所有应收款
        return queryset.filter(client=value)

    class Meta:
        model = Account_Due
        fields = ['client', 'greater_not_cancel']


class ReceiptFilters(django_filters.rest_framework.FilterSet):
    ord_num = django_filters.CharFilter(field_name='ord_num')
    settlement_num = django_filters.CharFilter(field_name='settlement_num')

    class Meta:
        model = Receipt
        fields = ['ord_num', 'settlement_num']


class PaymentFilters(django_filters.rest_framework.FilterSet):
    ord_num = django_filters.CharFilter(field_name='ord_num')
    settlement_num = django_filters.CharFilter(field_name='settlement_num')

    class Meta:
        model = Payment
        fields = ['ord_num', 'settlement_num']
