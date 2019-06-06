import xadmin

from .models import Sale, SaleOrder, SaleExport


class SaleAdmin:
    list_display = ['ord_num', 'woolens', 'client', 'sale_num', 'sale_price', 'sale_total', 'ord_date',
                    'proceeds', 'arrear', ]
    search_fields = ['ord_num', 'client']


class SaleOrderAdmin:
    list_display = ['ord_num', 'woolens', 'client', 'sale_num', 'sale_price', 'sale_total', 'ord_date',
                    'proceeds', 'remain', ]
    search_fields = ['ord_num', 'client']


class SaleExportAdmin:
    list_display = ['ord_num', 'sale_order', 'ord_date', 'take_num', 'take_price', 'take_total']


xadmin.site.register(Sale, SaleAdmin)
xadmin.site.register(SaleOrder, SaleOrderAdmin)
xadmin.site.register(SaleExport, SaleExportAdmin)

