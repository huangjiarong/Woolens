from rest_framework import mixins, viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.views.generic.base import TemplateView

from .models import Reeling, ReelingReturn
from .serializers import ReelingReturnSerializers, ReelingSerializers,\
    CompleteReturnReelingSerializer
from .filters import ReelingFilter, ReelingReturnFilter
from hairing.views import NewCreateMixin


#分页
class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class ReelingView(TemplateView):
    template_name = 'reeling/alterReeling.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


class ReelingViewSets(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示摇纱领料哦
    create:
        创建摇纱领料, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = Reeling.objects.all().order_by('id')
    serializer_class = ReelingSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = ReelingFilter
    ordering_fields = ('id', )


class ReelingReturnViewSets(mixins.ListModelMixin, NewCreateMixin, viewsets.GenericViewSet):
    """
    list:
        显示摇纱回毛
    create:
        创建摇纱回毛, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    queryset = ReelingReturn.objects.all().order_by('id')
    serializer_class = ReelingReturnSerializers
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = ReelingReturnFilter


class Complete_Return_Reeling(views.APIView):
    def post(self, request):
        serializer = CompleteReturnReelingSerializer(many=True, data=request.data)
        if serializer.is_valid(raise_exception=False):
            for data in serializer.data:
                data.pop('index', -1)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

