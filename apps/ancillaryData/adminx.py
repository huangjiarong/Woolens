import xadmin

from xadmin import views
from .models import ClientType, WoolensType, Color, Packaging, WarehouseType, Settlement


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = '毛料生产进销存后台管理系统'
    site_footer = 'by 黄佳荣'
    menu_style = 'accordion'

class ClientTypeAdmin(object):
    list_display = ['id', 'number', 'name', 'add_time', 'remarks', ]


class ColorAdmin(object):
    list_display = ['id', 'color', 'color_num', 'add_time', ]


class PackagingAdmin(object):
    list_display = ['id', 'name', 'number']


class SettlementAdmin(object):
    list_display = ['id', 'name', ]


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(ClientType, ClientTypeAdmin)
xadmin.site.register(WoolensType, ClientTypeAdmin)
xadmin.site.register(Color, ColorAdmin)
xadmin.site.register(Packaging, PackagingAdmin)
xadmin.site.register(WarehouseType, PackagingAdmin)
xadmin.site.register(Settlement, SettlementAdmin)

