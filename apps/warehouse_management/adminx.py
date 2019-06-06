import xadmin

from .models import Inventory, Transfers, Check


class InventoryAdmin:
    list_display = ['id', 'woolens_type', 'name', 'packaging', 'color', 'dyelot_num', 'batch_num',
                    'number', 'warehouse', 'assess_price']
    search_fields = ['name', 'woolens_type']


class CheckAdmin:
    list_display = ['warehouse', 'inventory', 'number', 'actual_num', 'difference', 'date']
    search_fields = ['warehouse', ]


class TransferAdmin:
    list_display = ['from_warehouse', 'to_warehouse', 'inventory', 'transfers_num', 'date']
    search_fields = ['from_warehouse', 'to_warehouse']


xadmin.site.register(Inventory, InventoryAdmin)
xadmin.site.register(Check, CheckAdmin)
xadmin.site.register(Transfers, TransferAdmin)
