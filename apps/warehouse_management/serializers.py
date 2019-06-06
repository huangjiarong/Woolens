from rest_framework import serializers

from .models import Inventory, Transfers, Check


class InventorySerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['price'] = instance.assess_price
        ret['remain'] = instance.number
        ret['packaging_name'] = instance.packaging.name
        ret['color_name'] = instance.color.color
        ret['color_num'] = instance.color.color_num
        ret['warehouse_name'] = instance.warehouse.name
        return ret

    class Meta:
        model = Inventory
        fields = '__all__'


class TransfersListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        """
        attrs数据类型为[
            {inventory: InventoryObjects(1), transfers_num: 100, ...},
            {inventory: InventoryObjects(2), transfers_num: 200, ...},
            {inventory: InventoryObjects(1), transfers_num: 50, ...},
        ]
        1.构造两个空列表存放对应的库存对象和取货数量:
            goods_lst = [
                InventoryObjects(1),InventoryObjects(2), InventoryObjects(1)
            ]
            take_num_lst = [
                100, 200, 50
            ]
        2.构建一个dict, 结构为:goods_takenum_map = {
            InventoryObjects(1): 150, InventoryObjects(2): 100
        }
        3.遍历dict, 对transfers_num和库存的数量number进行比较即可
        """
        goods_takenum_map = {}
        goods_lst, take_num_lst = [], []
        for transfers in attrs:
            goods_lst.append(transfers['inventory'])
            take_num_lst.append(transfers['transfers_num'])

        for goods_takenum in zip(goods_lst, take_num_lst):
            if goods_takenum[0] not in goods_takenum_map.keys():
                goods_takenum_map[goods_takenum[0]] = goods_takenum[1]
            else:
                goods_takenum_map[goods_takenum[0]] += goods_takenum[1]

        for goods, take_num in goods_takenum_map.items():
            if goods.number < take_num:
                raise serializers.ValidationError('总的调拨数量大于库存')
        return attrs


class TransfersSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def validate(self, attrs):
        if not (set(attrs['to_warehouse'].type.all()) & set(attrs['from_warehouse'].type.all())):
            raise serializers.ValidationError('错误: 调出仓库和调入仓库并非同种类型的仓库!')
        if attrs['transfers_num'] > attrs['inventory'].number:
            raise serializers.ValidationError('错误: 调拨数量大于库存量')
        if attrs['inventory'] not in attrs['from_warehouse'].inventory.all():
            raise serializers.ValidationError('错误: 调拨的毛料不在调出仓库!')
        if attrs['from_warehouse'] == attrs['to_warehouse']:
            raise serializers.ValidationError('错误: 调出仓库不能和调入仓库一样')
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.inventory.name
        ret['packaging_name'] = instance.inventory.packaging.name
        ret['color_name'] = instance.inventory.color.color
        ret['color_num'] = instance.inventory.color.color_num
        ret['dyelot_num'] = instance.inventory.dyelot_num
        ret['batch_num'] = instance.inventory.batch_num
        ret['from_warehouse_name'] = instance.from_warehouse.name
        ret['to_warehouse_name'] = instance.to_warehouse.name
        return ret

    def create(self, validated_data):
        transfers = Transfers.objects.create(**validated_data)
        validated_data['inventory'].number -= validated_data['transfers_num']

        data = {}
        data['name'] = validated_data['inventory'].name
        data['packaging'] = validated_data['inventory'].packaging
        data['color'] = validated_data['inventory'].color
        data['dyelot_num'] = validated_data['inventory'].dyelot_num
        data['batch_num'] = validated_data['inventory'].batch_num
        data['woolens_type'] = validated_data['inventory'].woolens_type
        data['warehouse'] = validated_data['to_warehouse']
        to_warehouse_inventory, created = Inventory.objects.get_or_create(**data)
        if not created:
            to_warehouse_inventory.number += validated_data['transfers_num']

        validated_data['inventory'].save()
        to_warehouse_inventory.save()

        return transfers


    class Meta:
        model = Transfers
        list_serializer_class = TransfersListSerializer
        fields = '__all__'


class CheckSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def validate(self, attrs):
        if attrs['inventory'].warehouse != attrs['warehouse']:
            raise serializers.ValidationError('所选毛料不在所选的仓库中!')
        return attrs

    def create(self, validated_data):
        validated_data['number'] = validated_data['inventory'].number
        validated_data['difference'] = validated_data['actual_num'] - validated_data['number']
        check = Check.objects.create(**validated_data)
        return check

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.inventory.name
        ret['color_name'] = instance.inventory.color.color
        ret['color_num'] = instance.inventory.color.color_num
        ret['packaging_name'] = instance.inventory.packaging.name
        ret['dyelot_num'] = instance.inventory.dyelot_num
        ret['batch_num'] = instance.inventory.batch_num
        ret['warehouse_name'] = instance.warehouse.name
        return ret

    class Meta:
        model = Check
        fields = '__all__'
        read_only_fields = ('difference', 'number', )
