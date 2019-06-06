from rest_framework import mixins, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Due, Payment, Account_Due, Receipt
from .serializers import DueSerializer, PaymentSerializer, AccountDueSerializer, ReceiptSerializer
from .filters import DueFilters, AccountDueFilters, ReceiptFilters, PaymentFilters
from hairing.views import NewCreateMixin


#分页
class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


@method_decorator(login_required, name='dispatch')
class NewTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


class DueViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示应付款
    """
    queryset = Due.objects.all().order_by('-id')
    serializer_class = DueSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = DueFilters
    ordering_fields = ('id', )


class PaymentViewSet(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示付款单
    list:
        创建付款单, 可创建多个对象
    """
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = PaymentFilters
    ordering_fields = ('id', )


class AccountDueViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示应收款
    """
    queryset = Account_Due.objects.all().order_by('-id')
    serializer_class = AccountDueSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = AccountDueFilters
    ordering_fields = ('id', )


class ReceiptViewSet(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示收款单
    list:
        创建收款单, 可创建多个对象
    """
    queryset = Receipt.objects.all().order_by('-id')
    serializer_class = ReceiptSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ReceiptFilters
    ordering_fields = ('id', )
