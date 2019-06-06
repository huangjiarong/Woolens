import xadmin

from .models import Reeling, ReelingReturn


class ReelingAdmin(object):
    list_display = ['id', 'ord_num', 'material', 'number', 'price', 'total_price', 'process',]


class ReelingReturnAdmin(object):
    list_display = ['id', 'ord_num', 'reeling', 'name', 'number', 'price', 'warehouse']


# class ReelingWarehouseAdmin(object):
#     list_display = ['name', 'packaging', 'color', 'dyelot_num', 'batch_num',
#                     'number', 'warehouse', ]


xadmin.site.register(Reeling, ReelingAdmin)
xadmin.site.register(ReelingReturn, ReelingReturnAdmin)
# xadmin.site.register(ReelingWarehouse, ReelingWarehouseAdmin)
