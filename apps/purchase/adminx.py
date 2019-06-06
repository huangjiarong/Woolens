import xadmin

from .models import PurchaseOrder, Purchase, TakeGoods

class PurchaseOrderAdmin(object):
    list_display = ['ord_num', 'woolens', 'number', 'price', 'total', 'supplier', 'remain',
                    'complete_return', 'order_date', ]
    search_fields = ['ord_num', 'woolens', 'supplier']


class TakeGoodsAdmin(object):
    list_display = ['ord_num', 'purchase_order', 'name', 'packaging', 'color',
                    'dyelot_num', 'batch_num', 'take_num', 'take_price', 'take_total',
                    'take_date', 'warehouse', 'complete_return']
    search_fields = ['ord_num', 'purchase_order']



class PurchaseAdmin:
    list_display = ['ord_num', 'woolens', 'number', 'price', 'total', 'supplier', 'warehouse',
                    'date', 'source_orderNum', ]
    search_fields = ['ord_num', 'woolens', 'supplier', 'source_orderNum']


xadmin.site.register(PurchaseOrder, PurchaseOrderAdmin)
xadmin.site.register(Purchase, PurchaseAdmin)
xadmin.site.register(TakeGoods, TakeGoodsAdmin)
