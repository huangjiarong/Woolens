from rest_framework import mixins, viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.views.generic.base import TemplateView

from .models import Dye, DyeReturn, DyeNotice
from .serializers import DyeSerializers, DyeNoticeSerializers, DyeReturnSerializers,\
     CompleteReturnDyeSerializer
from .filters import DyeFilter, DyeNoticeFilter, DyeReturnFilter
from hairing.views import NewCreateMixin


#分页
class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class DyeView(TemplateView):
    template_name = 'dye/alterDye.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


class DyeViewSets(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示染色领料
    create:
        创建染色领料, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Dye.objects.all().order_by('id')
    serializer_class = DyeSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = DyeFilter
    ordering_fields = ('id', )

class DyeNoticeViewSets(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示染色通知单
    create:
        创建染色通知单, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = DyeNotice.objects.all().order_by('id')
    serializer_class = DyeNoticeSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = DyeNoticeFilter



class DyeReturnViewSets(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示染色回毛
    create:
        创建染色回毛, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = DyeReturn.objects.all().order_by('id')
    serializer_class = DyeReturnSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = DyeReturnFilter


class Complete_Return_Dye(views.APIView):
    def post(self, request):
        serializer = CompleteReturnDyeSerializer(many=True, data=request.data)
        if serializer.is_valid(raise_exception=False):
            for data in serializer.data:
                data.pop('index', -1)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
