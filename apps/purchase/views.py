from rest_framework import mixins, viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import PurchaseOrder, Purchase, TakeGoods
from .serializers import PurchaseOrderSerializers, PurchaseSerializers, TakeGoodsSerializers, \
    CompleteReturnPurchaseSerializer
from .filters import PurchaseOrderFilter, TakeGoodsFilter, PurchaseFilter
from hairing.views import NewCreateMixin
from users.views import LoginRequiredMixin

@method_decorator(login_required, name='dispatch')
class PurchaseOrderView(TemplateView):
    template_name = 'purchase/alterPurchaseOrder.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


class PurchaseView(TemplateView):
    template_name = 'purchase/alterPurchase.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ord_num'] = request.GET.get('ord_num', '')
        return self.render_to_response(context)


#分页
class Pagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'pageIndex'


class PurchaseViewSets(viewsets.GenericViewSet, NewCreateMixin, mixins.ListModelMixin):
    """
    list:
        显示购货单
    create:
        创建购货单, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    serializer_class = PurchaseSerializers
    queryset = Purchase.objects.all().order_by('-id')
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = PurchaseFilter


class PurchaseOrderViewSets(viewsets.GenericViewSet, NewCreateMixin, mixins.ListModelMixin):
    """
    list:
        显示购货订单
    create:
        创建购货订单, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    serializer_class = PurchaseOrderSerializers
    queryset = PurchaseOrder.objects.all().order_by('-id')
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = PurchaseOrderFilter
    ordering_fields = ('id', )


class TakeGoodsViewSets(viewsets.GenericViewSet, NewCreateMixin, mixins.ListModelMixin):
    """
    list:
        显示取货
    create:
        创建取货记录, 可接收两种类型:
        {'name': '111'} 或者 [{'name': '111'}, {'name': '222'}]
    """
    serializer_class = TakeGoodsSerializers
    queryset = TakeGoods.objects.all().order_by('-id')
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = TakeGoodsFilter


class Complete_Return_Purchase(views.APIView):
    def post(self, request):
        serializer = CompleteReturnPurchaseSerializer(many=True, data=request.data)
        if serializer.is_valid(raise_exception=False):
            for data in serializer.data:
                data.pop('index', -1)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


