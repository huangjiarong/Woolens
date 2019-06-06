import xadmin

from .models import Hairing, HairingReturn


class HairingAdmin:
    list_display = ['id', 'ord_num', 'dye_goods', 'number', 'price', 'process',]


class HairingReturnAdmin:
    list_display = ['id', 'ord_num', 'hairing', 'name', 'number', 'price', 'warehouse']


xadmin.site.register(Hairing, HairingAdmin)
xadmin.site.register(HairingReturn, HairingReturnAdmin)
