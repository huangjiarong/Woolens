from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.views.generic.base import TemplateView

from .models import Sale, SaleOrder, SaleExport
from .serializers import SaleSerializer, SaleOrderSerializer, SaleExportSerializer
from .filters import SaleOrderFilter, SaleFilter
from hairing.views import NewCreateMixin


#分页
class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class SaleView(TemplateView):
    template_name = 'sale/alterSale.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


class SaleOrderView(TemplateView):
    template_name = 'sale/alterSaleOrder.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


class SaleViewSet(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示销货单
    create:
        创建销货单, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    serializer_class = SaleSerializer
    queryset = Sale.objects.all().order_by('-id')
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = SaleFilter
    ordering_fields = ('id', )


class SaleOrderViewSet(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示销货订单
    create:
        创建销货订单, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    serializer_class = SaleOrderSerializer
    queryset = SaleOrder.objects.all().order_by('-id')
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = SaleOrderFilter
    ordering_fields = ('id', )


class SaleExportViewSet(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示销货出库单
    create:
        创建销货出库单, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    serializer_class = SaleExportSerializer
    queryset = SaleExport.objects.all().order_by('-id')
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('ord_num', )
    ordering_fields = ('id', )
