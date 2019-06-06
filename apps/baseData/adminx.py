import xadmin

from .models import Warehouse, Woolens, Client, Staff, Account

class ClientAdmin:
    list_display = ['number', 'name', 'address', 'link_man', 'telephone', 'email', 'credit_limit',
                    'type', 'pre_receivable', 'receivable', ]
    search_fields = ['number', 'name']


class WarehouseAdmin(object):
    list_display = ['number', 'name', 'type', 'if_forbidden', 'if_default',
                     'area', ]
    search_fields = ['number', 'name']


class WoolensAdmin(object):
    list_display = ['name', 'type', 'number', 'cost', 'price', 'packaging', 'color', 'dyelot_num',
                    'batch_num', ]
    search_fields = ['number', 'name']


class StaffAdmin:
    list_display = ['username', 'name', 'number', 'email', 'telephone', 'phone', 'department', 'role',]
    search_fields = ['number', 'name', 'username']


class AccountAdmin:
    list_display = ['client', 'number', 'name', 'cur_balance', 'pre_balance']
    search_fields = ['number', 'name', ]


xadmin.site.register(Warehouse, WarehouseAdmin)
xadmin.site.register(Woolens, WoolensAdmin)
xadmin.site.register(Client, ClientAdmin)
xadmin.site.register(Staff, StaffAdmin)
xadmin.site.register(Account, AccountAdmin)
