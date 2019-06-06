from rest_framework import serializers

from .models import WoolensType, Color, ClientType, \
    WarehouseType, Packaging, Settlement


class ClientTypeSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    class Meta:
        model = ClientType
        fields = '__all__'


class WoolensTypeSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    class Meta:
        model = WoolensType
        fields = '__all__'


class ColorSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    class Meta:
        model = Color
        fields = '__all__'


class WarehouseTypeSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    class Meta:
        model = WarehouseType
        fields = '__all__'


class PackagingSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    class Meta:
        model = Packaging
        fields = '__all__'


class SettlementSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    class Meta:
        model = Settlement
        fields = '__all__'

