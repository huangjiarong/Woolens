from rest_framework import mixins, viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.views.generic.base import TemplateView

from .models import Hairing, HairingReturn
from .serializers import HairingSerializers, HairingReturnSerializer, CompleteReturnHairingSerializer
from .filters import HairingFilter, HairingReturnFilter


class NewCreateMixin(mixins.CreateModelMixin):
    """
    重写CreateModelMixin的create方法,可同时接受[{}, {}]类型和{}类型的数据
    接受多对象数据时出错会返回接收到的index,以便前端用于定位
    """
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True, allow_empty=False)
            if not serializer.is_valid(raise_exception=False):
                if isinstance(serializer.errors, dict):
                    #如果是ListSerializer里的错误则会返回dict类型
                    return Response(serializer.errors, headers={}, status=status.HTTP_400_BAD_REQUEST)
                #将index加入到错误信息里，以便前端定位到出错的行
                for index, value in enumerate(serializer.errors):
                    value['index'] = serializer.initial_data[index].get('index', '-1')
                return Response(serializer.errors, headers={}, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#分页
class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class HairingView(TemplateView):
    template_name = 'hairing/alterHairing.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


class HairingViewSets(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示打毛领料
    create:
        创建打毛领料, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Hairing.objects.all().order_by('id')
    serializer_class = HairingSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = HairingFilter
    ordering_fields = ('id', )


class HairingReturnViewSets(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示打毛回毛
    create:
        创建打毛回毛, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = HairingReturn.objects.all().order_by('id')
    serializer_class = HairingReturnSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = HairingReturnFilter


# class HairingWarehouseViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = HairingWarehouse.objects.all().order_by('id')
#     serializer_class = HairingWarehouseSerializer
#     pagination_class = Pagination


class Complete_Return_Hairing(views.APIView):
    def post(self, request):
        serializer = CompleteReturnHairingSerializer(many=True, data=request.data)
        if serializer.is_valid(raise_exception=False):
            for data in serializer.data:
                data.pop('index', -1)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
