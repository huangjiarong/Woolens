from rest_framework import viewsets, mixins
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Inventory, Transfers, Check
from .serializers import InventorySerializers, TransfersSerializer, CheckSerializer
from .filters import InventoryFilter, TransfersFilter, CheckFilter
from hairing.views import NewCreateMixin


#分页
class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class InventoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示库存
    """
    queryset = Inventory.objects.all().order_by('id')
    serializer_class = InventorySerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = InventoryFilter
    ordering_fields = ('id', 'woolens_type')


class TransfersViewSet(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示调拨单
    create:
        创建调拨单
    """
    queryset = Transfers.objects.all().order_by('id')
    serializer_class = TransfersSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = TransfersFilter


class CheckViewSet(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示盘点
    create:
        创建盘点
    """
    queryset = Check.objects.all().order_by('id')
    serializer_class = CheckSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = CheckFilter
