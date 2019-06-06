from rest_framework import serializers
from .models import Client, Woolens, Warehouse, Staff, Account


# class ClientListSerializers(serializers.ListSerializer):
#     def create(self, validated_data):
#         print('hello world')
#         client = [Client(**item) for item in validated_data]
#         return Client.objects.bulk_create(client)
#
# class ClientSerializers(serializers.ModelSerializer):
#     add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
#     class Meta:
#         model = Client
#         fields = '__all__'


class ClientSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        type_id = []
        type_name = ''
        for type in instance.type.all():
            type_name += (type.name + ', ')
            type_id.append(type.id)
        ret['type'] = type_name.rstrip(', ')
        ret['client_type'] = type_id[0]
        return ret

    class Meta:
        model = Client
        fields = '__all__'


class WarehouseSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        type_id = []
        for type in instance.type.all():
            type_id.append(type.id)
        ret['type'] = type_id[0]
        return ret

    class Meta:
        model = Warehouse
        fields = '__all__'


class WoolensSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    class Meta:
        model = Woolens
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # ret['woolens_number'] = instance.number
        # ret['woolens'] = instance.id
        ret['get_color'] = str(instance.color.id) + ',' + instance.color.color_num
        ret['color_num'] = instance.color.color_num
        ret['color_name'] = instance.color.color
        ret['packaging_name'] = instance.packaging.name
        return ret


class AccountSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    class Meta:
        model = Account
        fields = '__all__'


class StaffSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ('login_times', 'operate')
