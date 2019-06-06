from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import ClientType, WoolensType, Color, WarehouseType, Packaging,\
    Settlement
from .serializers import ClientTypeSerializers, WoolensTypeSerializers,\
    ColorSerializers, WarehouseTypeSerializers, PackagingSerializers,\
    SettlementSerializers
from hairing.views import NewCreateMixin
from .filters import PackagingFilter


class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class ClientTypeViewSet(mixins.ListModelMixin, NewCreateMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示客户类别
    create:
        创建客户类别,支持创建多个实例, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    patch:
        修改客户类别, 只支持单个实例的修改
    delete:
        删除客户类别, 只支持单个实例的删除
    """
    queryset = ClientType.objects.all().order_by('-id')
    serializer_class = ClientTypeSerializers
    pagination_class = Pagination


class WoolensTypeViewSet(mixins.ListModelMixin, NewCreateMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示毛料类别
    create:
        创建毛料类别, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    patch:
        修改毛料类别, 只支持单个实例的修改
    delete:
        删除毛料类别, 只支持单个实例的删除
    """
    queryset = WoolensType.objects.all().order_by('-id')
    serializer_class = WoolensTypeSerializers
    pagination_class = Pagination


class ColorViewSet(viewsets.GenericViewSet, NewCreateMixin, mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin, mixins.ListModelMixin):
    """
    list:
        显示颜色
    create:
        创建颜色, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    patch:
        修改颜色, 只支持单个实例的修改
    delete:
        删除颜色, 只支持单个实例的删除
    """
    queryset = Color.objects.all().order_by('-id')
    serializer_class = ColorSerializers
    pagination_class = Pagination


class WarehouseTypeViewSet(viewsets.GenericViewSet, NewCreateMixin, mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin, mixins.ListModelMixin):
    """
    list:
        显示仓库类别
    create:
        创建仓库类别, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    patch:
        修改仓库类别, 只支持单个实例的修改
    delete:
        删除仓库类别, 只支持单个实例的删除
    """
    queryset = WarehouseType.objects.all().order_by('-id')
    serializer_class = WarehouseTypeSerializers
    pagination_class = Pagination


class PackagingViewSet(viewsets.GenericViewSet, NewCreateMixin, mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin, mixins.ListModelMixin):
    """
    list:
        显示包装类别
    create:
        创建包装类别, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    patch:
        修改包装类别, 只支持单个实例的修改
    delete:
        删除包装类别, 只支持单个实例的删除
    """
    queryset = Packaging.objects.all().order_by('-id')
    serializer_class = PackagingSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = PackagingFilter


class SettlementViewSet(viewsets.GenericViewSet, NewCreateMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, mixins.ListModelMixin):
    """
    list:
        显示结算方式
    create:
        创建结算方式, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    patch:
        修改结算方式, 只支持单个实例的修改
    delete:
        删除结算方式, 只支持单个实例的删除
    """
    queryset = Settlement.objects.all().order_by('-id')
    serializer_class = SettlementSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
