import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Woolens.settings")

import django
django.setup()

from db_tools.data.ancillay_data import color_data, packaging_data, warehouseType_data, \
    clientType_data, woolensType_data

from ancillaryData.models import Color, Packaging, WarehouseType, ClientType, WoolensType

for color in color_data:
    Color.objects.create(**color)

for packaging in packaging_data:
    Packaging.objects.create(**packaging)

for warehouse_type in warehouseType_data:
    WarehouseType.objects.create(**warehouse_type)

for clientType in clientType_data:
    ClientType.objects.create(**clientType)

for woolensType in woolensType_data:
    WoolensType.objects.create(**woolensType)
