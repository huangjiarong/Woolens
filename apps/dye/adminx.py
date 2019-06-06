import xadmin

from .models import Dye, DyeNotice, DyeReturn


class DyeAdmin:
    list_display = ['id', 'ord_num', 'reeling', 'remain', 'number', 'price', 'process',
                    'ord_date', 'return_date', 'complete_return']


class DyeNoticeAdmin:
    list_display = ['id', 'ord_num', 'dye', 'name', 'packaging', 'dyelot_num', 'batch_num',
                    'color', 'dye_color', 'ord_date', 'return_date', 'number', 'price',
                    'complete_return']


class DyeReturnAdmin:
    list_display = ['id', 'ord_num', 'dye_notice', 'name', 'packaging', 'color', 'dyelot_num',
                    'batch_num', 'number', 'price', ]


# class DyeWarehouseAdmin:
#     list_display = ['id', 'name', 'packaging', 'color', 'dyelot_num', 'batch_num', 'number',
#                     'assess_price', ]


xadmin.site.register(Dye, DyeAdmin)
xadmin.site.register(DyeNotice, DyeNoticeAdmin)
xadmin.site.register(DyeReturn, DyeReturnAdmin)
# xadmin.site.register(DyeWarehouse, DyeWarehouseAdmin)
