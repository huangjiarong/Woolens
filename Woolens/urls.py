"""Woolens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from guardian.decorators import permission_required_or_403
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

import xadmin
from ancillaryData.views import WoolensTypeViewSet, ClientTypeViewSet,\
    ColorViewSet, WarehouseTypeViewSet, PackagingViewSet, SettlementViewSet
from baseData.views import WarehouseViewSets, ClientViewSets, WoolensViewSets, AccountViewSets,\
    StaffViewSets
from purchase.views import PurchaseOrderViewSets, PurchaseOrderView, TakeGoodsViewSets,\
    Complete_Return_Purchase, PurchaseViewSets, PurchaseView
from reeling.views import ReelingViewSets, ReelingReturnViewSets, ReelingView,\
    Complete_Return_Reeling
from dye.views import DyeView, DyeViewSets, DyeNoticeViewSets, DyeReturnViewSets,\
    Complete_Return_Dye
from hairing.views import HairingViewSets, HairingView, HairingReturnViewSets,\
    Complete_Return_Hairing
from warehouse_management.views import InventoryViewSet, TransfersViewSet, CheckViewSet
from money_management.views import NewTemplateView, DueViewSet, PaymentViewSet, \
    AccountDueViewSet, ReceiptViewSet
from sale.views import SaleViewSet, SaleView, SaleOrderViewSet, SaleOrderView,\
    SaleExportViewSet
from users.views import LoginView, LogoutView

router = DefaultRouter()

#配置ancillaryData的api
router.register(r'woolensType', WoolensTypeViewSet, base_name='woolensType')
router.register(r'clientType', ClientTypeViewSet, base_name='clientType')
router.register(r'color', ColorViewSet, base_name='color')
router.register(r'warehouseType', WarehouseTypeViewSet, base_name='warehouseType')
router.register(r'packaging', PackagingViewSet, base_name='packaging')
router.register(r'settlement', SettlementViewSet, base_name='settlement')

#配置baseData的api
router.register(r'client', ClientViewSets, base_name='client')
router.register(r'warehouse', WarehouseViewSets, base_name='warehouse')
router.register(r'woolens', WoolensViewSets, base_name='woolens')
router.register(r'account', AccountViewSets, base_name='account')
router.register(r'staff', StaffViewSets, base_name='staff')

#配置purchase的api
router.register(r'purchase', PurchaseViewSets, base_name='purchase')
router.register(r'purchaseOrder', PurchaseOrderViewSets, base_name='purchaseOrder')
router.register(r'take_goods', TakeGoodsViewSets, base_name='take_goods')

#配置sale的api
router.register(r'sale', SaleViewSet, base_name='sale')
router.register(r'saleOrder', SaleOrderViewSet, base_name='saleOrder')
router.register(r'saleExport', SaleExportViewSet, base_name='saleExport')

#配置reeling的api
router.register(r'reeling', ReelingViewSets, base_name='reeling')
router.register(r'reelingReturn', ReelingReturnViewSets, base_name='reelingReturn')

#配置dye的api
router.register(r'dye', DyeViewSets, base_name='dye')
router.register(r'dyeNotice', DyeNoticeViewSets, base_name='dyeNotice')
router.register(r'dyeReturn', DyeReturnViewSets, base_name='dyeReturn')

#配置hairing的api
router.register(r'hairing', HairingViewSets, base_name='hairing')
router.register(r'hairingReturn', HairingReturnViewSets, base_name='hairingReturn')

#配置warehouse_management的api
router.register(r'inventory', InventoryViewSet, base_name='inventory')
router.register(r'transfers', TransfersViewSet, base_name='transfers')
router.register(r'check', CheckViewSet, base_name='check')

#配置money_management的api
router.register(r'due', DueViewSet, base_name='due')
router.register(r'payment', PaymentViewSet, base_name='payment')
router.register(r'account_due', AccountDueViewSet, base_name='account_due')
router.register(r'receipt', ReceiptViewSet, base_name='receipt')


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('api/docs/', include_docs_urls(title='Woolens')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('', NewTemplateView.as_view(template_name='index.html'), name='index'),
    path('login', TemplateView.as_view(template_name='users/login.html'), name='login'),
    path('user_login', LoginView.as_view(), name='user_login'),
    path('logout', LogoutView.as_view(), name='logout'),
]

#购货管理的url
purchase_urls = [
    path('purchase', permission_required_or_403('purchase.view_purchase')
    (NewTemplateView.as_view(template_name='purchase/purchaseList.html')), name="purchaseList"),
    path('purchaseOrder', permission_required_or_403('purchase.view_purchaseorder')
    (NewTemplateView.as_view(template_name='purchase/purchaseOrderList.html')), name="purchaseOrderList"),
    path('alterpurchaseOrder/', permission_required_or_403('purchase.add_purchaseorder')
    (PurchaseOrderView.as_view()), name='alertpurchaseOrder'),
    path('alterPurchase/', permission_required_or_403('purchase.add_purchase')
    (PurchaseView.as_view()), name='alterPurchase'),
    path('complete_return_purchase', Complete_Return_Purchase.as_view(), name='complete_return_purchase'),
]

#辅助资料的url
ancillaryData_urls = [
    path('clientType', permission_required_or_403('ancillaydata.view_clientType')
    (NewTemplateView.as_view(template_name='ancillaryData/clientType.html')), name="clientTypeList"),
    path('woolensType', permission_required_or_403('ancillaydata.view_woolensType')
    (NewTemplateView.as_view(template_name='ancillaryData/woolensType.html')), name="woolensTypeList"),
    path('warehouseType', permission_required_or_403('ancillaydata.view_warehouseType')
    (NewTemplateView.as_view(template_name='ancillaryData/warehouseType.html')), name="warehouseTypeList"),
    path('color', permission_required_or_403('ancillaydata.view_color')
    (NewTemplateView.as_view(template_name='ancillaryData/color.html')), name="colorList"),
    path('packaging', permission_required_or_403('ancillaydata.view_packaging')
    (NewTemplateView.as_view(template_name='ancillaryData/packaging.html')), name="packagingList"),
    path('settlement', permission_required_or_403('ancillaydata.view_settlement')
    (NewTemplateView.as_view(template_name='ancillaryData/settlement.html')), name="settlementList"),
]

#销货管理的url
sale_urls = [
    path('sale', permission_required_or_403('sale.view_sale')
    (NewTemplateView.as_view(template_name='sale/saleList.html')), name="saleList"),
    path('saleOrder', permission_required_or_403('sale.view_saleorder')
    (NewTemplateView.as_view(template_name='sale/saleOrderList.html')), name="saleOrder"),
    path('alterSale/', permission_required_or_403('sale.add_sale')
    (SaleView.as_view()), name="alterSale"),
    path('addSaleOrder', permission_required_or_403('sale.add_saleorder')
    (SaleOrderView.as_view()), name="addSaleOrder"),
    path('saleOrder/', permission_required_or_403('sale.view_saleorder')
    (SaleOrderView.as_view()),),
]

#基础资料的url
baseData_urls = [
    path('client', permission_required_or_403('basedata.view_client')
    (NewTemplateView.as_view(template_name='baseData/client.html')), name="clientList"),
    path('warehouse', permission_required_or_403('basedata.view_warehouse')
    (NewTemplateView.as_view(template_name='baseData/warehouse.html')), name="warehouseList"),
    path('woolens', permission_required_or_403('basedata.view_woolens')
    (NewTemplateView.as_view(template_name='baseData/woolens.html')), name="woolensList"),
    path('account', permission_required_or_403('basedata.view_account')
    (NewTemplateView.as_view(template_name='baseData/account.html')), name="accountList"),
    path('staff', permission_required_or_403('basedata.view_staff')
    (NewTemplateView.as_view(template_name='baseData/staff.html')), name="staffList"),
]

#资金管理的url
money_management_urls = [
    path('payment', permission_required_or_403('money_management.view_payment')
    (NewTemplateView.as_view(template_name='money_management/paymentList.html')), name="paymentList"),
    path('addPayment/', permission_required_or_403('money_management.add_payment')
    (NewTemplateView.as_view(template_name='money_management/addPayment.html')), name="addPayment"),
    path('payment/', permission_required_or_403('money_management.view_payment')
    (NewTemplateView.as_view(template_name='money_management/paymentDetail.html'))),
    path('receipt', permission_required_or_403('money_management.view_receipt')
    (NewTemplateView.as_view(template_name='money_management/receiptList.html')), name="receiptList"),
    path('addReceipt/', permission_required_or_403('money_management.add_receipt')
    (NewTemplateView.as_view(template_name='money_management/addReceipt.html')), name="addReceipt"),
    path('receipt/', permission_required_or_403('money_management.view_receipt')
    (NewTemplateView.as_view(template_name='money_management/receiptDetail.html'))),
]

#仓库管理的url
warehouse_management_urls = [
    path('inventory', permission_required_or_403('warehouse_management.view_inventory')
    (NewTemplateView.as_view(template_name='warehouse_management/inventory.html')), name="inventory"),
    path('transfers', permission_required_or_403('warehouse_management.view_transfers')
    (NewTemplateView.as_view(template_name='warehouse_management/transfers.html')), name="transfers"),
    path('addTransfers', permission_required_or_403('warehouse_management.add_transfers')
    (NewTemplateView.as_view(template_name='warehouse_management/addTransfers.html')), name="addTransfers"),
    path('check', permission_required_or_403('warehouse_management.view_check')
    (NewTemplateView.as_view(template_name='warehouse_management/check.html')), name="check"),
    path('addCheck', permission_required_or_403('warehouse_management.add_check')
    (NewTemplateView.as_view(template_name='warehouse_management/addCheck.html')), name="addCheck"),
]

#三个加工环节的url
process_urls = [
    path('reeling', permission_required_or_403('reeling.view_reeling')
    (NewTemplateView.as_view(template_name='reeling/reelingList.html')), name="reelingList"),
    path('dye', permission_required_or_403('dye.view_dye')
    (NewTemplateView.as_view(template_name='dye/dyeList.html')), name="dyeList"),
    path('hairing', permission_required_or_403('hairing.view_hairing')
    (NewTemplateView.as_view(template_name='hairing/hairingList.html')), name="hairingList"),
    path('alterReeling/', permission_required_or_403('reeling.add_reeling')
    (ReelingView.as_view()), name='alterReeling'),
    path('alterDye/', permission_required_or_403('dye.add_dye')
    (DyeView.as_view()), name='alterDye'),
    path('alterHairing/', permission_required_or_403('hairing.add_hairing')
    (HairingView.as_view()), name='alterHairing'),
    path('complete_return_reeling', Complete_Return_Reeling.as_view(), name='complete_return_reeling'),
    path('complete_return_dye', Complete_Return_Dye.as_view(), name='complete_return_dye'),
    path('complete_return_hairing', Complete_Return_Hairing.as_view(), name='complete_return_hairing'),
]

urlpatterns.extend(ancillaryData_urls)
urlpatterns.extend(purchase_urls)
urlpatterns.extend(sale_urls)
urlpatterns.extend(baseData_urls)
urlpatterns.extend(process_urls)
urlpatterns.extend(money_management_urls)
urlpatterns.extend(warehouse_management_urls)
