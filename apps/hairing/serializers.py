from rest_framework import serializers

from .models import Hairing, HairingReturn
from money_management.models import Due
from warehouse_management.models import Inventory


class HairingListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        """
        attrs数据类型为[
            {dye_goods: InventoryObjects(1), take_num: 100, ...},
            {dye_goods: InventoryObjects(2), take_num: 200, ...},
            {dye_goods: InventoryObjects(1), take_num: 50, ...},
        ]
        1.构造两个空列表存放对应的库存对象和取货数量:
            dye_goods_lst = [
                InventoryObjects(1),InventoryObjects(2), InventoryObjects(1)
            ]
            take_num_lst = [
                100, 200, 50
            ]
        2.构建一个dict, 结构为:goods_takenum_map = {
            InventoryObjects(1): 150, InventoryObjects(2): 100
        }
        3.遍历dict, 对take_num和库存的remain进行比较即可
        """
        goods_takenum_map = {}
        dye_goods_lst, take_num_lst = [], []
        for hairing in attrs:
            dye_goods_lst.append(hairing['dye_goods'])
            take_num_lst.append(hairing['number'])

        for goods_takenum in zip(dye_goods_lst, take_num_lst):
            if goods_takenum[0] not in goods_takenum_map.keys():
                goods_takenum_map[goods_takenum[0]] = goods_takenum[1]
            else:
                goods_takenum_map[goods_takenum[0]] += goods_takenum[1]

        for goods, take_num in goods_takenum_map.items():
            if goods.number < take_num:
                raise serializers.ValidationError('总的领料数量大于库存')
        return attrs

    def create(self, validated_data):
        print(validated_data)
        hairing_objs = [Hairing(**item) for item in validated_data]
        for hairing in hairing_objs:
            hairing.total_price = hairing.price * hairing.number
            hairing.dye_goods.number -= hairing.number
            hairing.dye_goods.save()
        print(hairing_objs)
        return Hairing.objects.bulk_create(hairing_objs)

class HairingSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    def validate(self, attrs):
        #对每条领料数据，将领料数量与仓库库存对比
        if attrs['number'] > attrs['dye_goods'].number:
            raise serializers.ValidationError('领料数量大于库存')
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.dye_goods.name
        ret['packaging_name'] = instance.dye_goods.packaging.name
        ret['color'] = instance.dye_goods.color.id
        ret['color_name'] = instance.dye_goods.color.color
        ret['color_num'] = instance.dye_goods.color.color_num
        ret['dyelot_num'] = instance.dye_goods.dyelot_num
        ret['batch_num'] = instance.dye_goods.batch_num
        ret['process_name'] = instance.process.name
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    class Meta:
        model = Hairing
        fields = '__all__'
        list_serializer_class = HairingListSerializer
        read_only_fields = ('total_price', 'complete_return', )


class HairingReturnSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['color_name'] = instance.color.color
        ret['color_num'] = instance.color.color_num
        ret['packaging_name'] = instance.packaging.name
        ret['process_name'] = instance.hairing.all()[0].process.name
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    def validate_hairing(self, hairing):
        """
        重写hairing的验证,每条hairing数据它们的订单号,加工厂以及确定毛料的字段需要一致
        """
        all = []
        ord_num_lst, name_lst, packaging_lst, color_lst, dyelot_num_lst, batch_num_lst, process_lst = (
            [], [], [], [], [], [], []
        )
        for r in hairing:
            ord_num_lst.append(r.ord_num)
            name_lst.append(r.dye_goods.name)
            packaging_lst.append(r.dye_goods.packaging)
            color_lst.append(r.dye_goods.color)
            batch_num_lst.append(r.dye_goods.batch_num)
            dyelot_num_lst.append(r.dye_goods.dyelot_num)
            process_lst.append(r.process)
        all.append(ord_num_lst)
        all.append(name_lst)
        all.append(packaging_lst)
        all.append(color_lst)
        all.append(dyelot_num_lst)
        all.append(batch_num_lst)
        all.append(process_lst)
        for tmp in all:
            if len(set(tmp)) != 1:
                raise serializers.ValidationError('所选数据的订单号和毛料需一致')
        return hairing

    def create(self, validated_data):
        #创建回毛记录
        validated_data['ord_num'] = validated_data['hairing'][0].ord_num
        validated_data['color'] = validated_data['hairing'][0].dye_goods.color
        validated_data['batch_num'] = validated_data['hairing'][0].dye_goods.batch_num
        validated_data['dyelot_num'] = validated_data['hairing'][0].dye_goods.dyelot_num
        validated_data['name'] = validated_data['hairing'][0].dye_goods.name
        validated_data['total'] = validated_data['price'] * validated_data['number']
        validated_data['process_total'] = validated_data['process_price'] * validated_data['number']
        validated_data['total_price'] = validated_data['total'] + validated_data['process_total']
        validated_data['assess_price'] = validated_data['price']
        hairing_objs = validated_data.pop('hairing')
        hairing_return = HairingReturn.objects.create(**validated_data)
        hairing_return.hairing.set(hairing_objs)

        #添加打毛产品进库
        data = {}
        data['name'] = hairing_return.name
        data['color'] = hairing_return.color
        data['packaging'] = hairing_return.packaging
        data['batch_num'] = hairing_return.batch_num
        data['dyelot_num'] = hairing_return.dyelot_num
        data['warehouse'] = hairing_return.warehouse
        inventory, created = Inventory.objects.get_or_create(**data)
        if not created:
            inventory.assess_price = (validated_data['total_price'] + inventory.number * inventory.assess_price) / (
                    validated_data['number'] + inventory.number)
            inventory.number += validated_data['number']
        else:
            inventory.woolens_type = '打毛产品'
            inventory.assess_price = validated_data['process_price'] + validated_data['price']
            inventory.number = validated_data['number']
        inventory.save()

        #取货完后需要新增或修改一条应付款记录
        due_dict = {}
        due_dict['source_ordNum'] = hairing_return.ord_num
        due_dict['client'] = hairing_objs[0].process
        due_dict['business_type'] = '打毛'
        due, created = Due.objects.get_or_create(**due_dict)
        if created:
            due.ord_num = hairing_return.ord_num
            due.date = hairing_return.return_date
            due.money = hairing_return.total_price
            due.not_cancel = hairing_return.total_price
        else:
            due.money += hairing_return.total_price
            due.not_cancel += hairing_return.total_price
        due.save()

        return hairing_return

    class Meta:
        model = HairingReturn
        fields = '__all__'
        read_only_fields = ('ord_num', 'name', 'color', 'dyelot_num', 'batch_num', 'total',
                            'assess_price', 'actual_price', 'process_total', 'total_price',
                            'process', 'complete_return', 'A', 'A1')


class CompleteReturnHairingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    index = serializers.IntegerField()

    def validate_id(self, id):
        try:
            hairing = Hairing.objects.get(id=id)
        except:
            raise serializers.ValidationError('id为{}的数据不存在'.format(id))
        return id

    def create(self, validated_data):
        #将打毛领料的complete_return字段设置为True
        hairing_obj = Hairing.objects.get(id=validated_data['id'])
        hairing_obj.complete_return = True
        hairing_obj.save()
        #将与该打毛领料单相连的染色通知单的complete_return也设置为True
        for return_obj in hairing_obj.hairing_return.all():
            return_obj.complete_return = True
            return_obj.save()
        return hairing_obj
