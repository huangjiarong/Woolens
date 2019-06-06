from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Client, Warehouse, Woolens, Account, Staff
from .serializers import WarehouseSerializers, ClientSerializers, WoolensSerializers, AccountSerializers,\
    StaffSerializers
from .filters import WoolensFilter, WarehouseFilter, ClientFilter, AccountFilter, StaffFilter
from hairing.views import NewCreateMixin


class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class ClientViewSets(mixins.ListModelMixin, NewCreateMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示客户
    create:
        创建客户, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Client.objects.all().order_by('-id')
    pagination_class = Pagination
    serializer_class = ClientSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = ClientFilter


class WarehouseViewSets(mixins.ListModelMixin, NewCreateMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示仓库
    create:
        创建仓库, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Warehouse.objects.all().order_by('-id')
    pagination_class = Pagination
    serializer_class = WarehouseSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = WarehouseFilter

class WoolensViewSets(mixins.ListModelMixin, NewCreateMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示毛料
    create:
        创建毛料, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Woolens.objects.all().order_by('-id')
    pagination_class = Pagination
    serializer_class = WoolensSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = WoolensFilter


class AccountViewSets(mixins.ListModelMixin, NewCreateMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示账户
    create:
        创建账户, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Account.objects.all().order_by('-id')
    pagination_class = Pagination
    serializer_class = AccountSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = AccountFilter


class StaffViewSets(mixins.ListModelMixin, NewCreateMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示账户
    create:
        创建账户, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Staff.objects.all().order_by('-id')
    pagination_class = Pagination
    serializer_class = StaffSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = StaffFilter
