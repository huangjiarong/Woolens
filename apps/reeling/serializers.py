from rest_framework import serializers

from .models import Reeling, ReelingReturn
from warehouse_management.models import Inventory
from money_management.models import Due


class ReelingListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        """
        attrs数据类型为[
            {material: InventoryObjects(1), take_num: 100, ...},
            {material: InventoryObjects(2), take_num: 200, ...},
            {material: InventoryObjects(1), take_num: 50, ...},
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
        3.遍历dict, 对take_num和库存的remain进行比较即可
        """
        goods_takenum_map = {}
        goods_lst, take_num_lst = [], []
        for reeling in attrs:
            goods_lst.append(reeling['material'])
            take_num_lst.append(reeling['number'])

        for goods_takenum in zip(goods_lst, take_num_lst):
            if goods_takenum[0] not in goods_takenum_map.keys():
                goods_takenum_map[goods_takenum[0]] = goods_takenum[1]
            else:
                goods_takenum_map[goods_takenum[0]] += goods_takenum[1]

        for goods, take_num in goods_takenum_map.items():
            if goods.number < take_num:
                raise serializers.ValidationError('总的领料数量大于库存')
        return attrs


class ReelingSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    def validate(self, attrs):
        if attrs['number'] > attrs['material'].number:
            raise serializers.ValidationError('领料数量大于订购数量')
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.material.name
        ret['packaging_name'] = instance.material.packaging.name
        ret['color'] = instance.material.color.id
        ret['color_name'] = instance.material.color.color
        ret['color_num'] = instance.material.color.color_num
        ret['dyelot_num'] = instance.material.dyelot_num
        ret['batch_num'] = instance.material.batch_num
        ret['process_name'] = instance.process.name
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    def create(self, validated_data):
        validated_data['total_price'] = validated_data['price'] * validated_data['number']
        reeling = Reeling.objects.create(**validated_data)
        #创建领料后减少库存数量
        validated_data['material'].number -= validated_data['number']
        validated_data['material'].save()
        return reeling

    class Meta:
        model = Reeling
        fields = '__all__'
        list_serializer_class = ReelingListSerializer
        read_only_fields = ('total_price', 'complete_return')


class ReelingReturnSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['color_name'] = instance.color.color
        ret['packaging_name'] = instance.packaging.name
        ret['color_num'] = instance.color.color_num
        ret['process_name'] = instance.reeling.first().process.name
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    def validate_reeling(self, reeling):
        """
        重写reeling的验证,每条数据的订单号以及毛料的字段需要相同才能通过验证
        """
        all = []
        ord_num_lst, name_lst, packaging_lst, color_lst, dyelot_num_lst, batch_num_lst = (
            [], [], [], [], [], []
        )
        for r in reeling:
            ord_num_lst.append(r.ord_num)
            name_lst.append(r.material.name)
            packaging_lst.append(r.material.packaging)
            color_lst.append(r.material.color)
            batch_num_lst.append(r.material.batch_num)
            dyelot_num_lst.append(r.material.dyelot_num)
        all.append(ord_num_lst)
        all.append(name_lst)
        all.append(packaging_lst)
        all.append(color_lst)
        all.append(dyelot_num_lst)
        all.append(batch_num_lst)
        for tmp in all:
            if len(set(tmp)) != 1:
                raise serializers.ValidationError('所选数据的订单号和毛料需一致')
        return reeling

    def create(self, validated_data):
        #创建回毛记录
        validated_data['ord_num'] = validated_data['reeling'][0].ord_num
        validated_data['color'] = validated_data['reeling'][0].material.color
        validated_data['batch_num'] = validated_data['reeling'][0].material.batch_num
        validated_data['dyelot_num'] = validated_data['reeling'][0].material.dyelot_num
        validated_data['name'] = validated_data['reeling'][0].material.name
        validated_data['total'] = validated_data['price'] * validated_data['number']
        validated_data['process_total'] = validated_data['process_price'] * validated_data['number']
        validated_data['total_price'] = validated_data['total'] + validated_data['process_total']
        validated_data['assess_price'] = validated_data['price']
        reeling_objs = validated_data.pop('reeling')
        reeling_return = ReelingReturn.objects.create(**validated_data)
        reeling_return.reeling.add(*reeling_objs)

        #添加摇纱产品进库
        data = {}
        data['name'] = reeling_return.name
        data['color'] = reeling_return.color
        data['packaging'] = reeling_return.packaging
        data['batch_num'] = reeling_return.batch_num
        data['dyelot_num'] = reeling_return.dyelot_num
        data['warehouse'] = reeling_return.warehouse
        inventory, created = Inventory.objects.get_or_create(**data)
        if not created:
            inventory.assess_price = (validated_data['total_price'] + inventory.number * inventory.assess_price) / (
                validated_data['number'] + inventory.number)
            inventory.number += validated_data['number']
        else:
            inventory.woolens_type = '摇纱产品'
            inventory.assess_price = validated_data['process_price'] + validated_data['price']
            inventory.number = validated_data['number']
        inventory.save()

        #取货完后需要新增或修改一条应付款记录
        due_dict = {}
        due_dict['source_ordNum'] = reeling_return.ord_num
        due_dict['client'] = reeling_objs[0].process
        due_dict['business_type'] = '摇纱'
        due, created = Due.objects.get_or_create(**due_dict)
        if created:
            due.ord_num = reeling_return.ord_num
            due.date = reeling_return.return_date
            due.money = reeling_return.total_price
            due.not_cancel = reeling_return.total_price
        else:
            due.money += reeling_return.total_price
            due.not_cancel += reeling_return.total_price
        due.save()

        return reeling_return


    class Meta:
        model = ReelingReturn
        fields = '__all__'
        read_only_fields = ('ord_num', 'name', 'color', 'dyelot_num', 'batch_num', 'total',
                            'assess_price', 'actual_price', 'A', 'A1', 'process_total', 'total_price',
                            'complete_return')


class CompleteReturnReelingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    index = serializers.IntegerField()

    def validate_id(self, id):
        try:
            reeling = Reeling.objects.get(id=id)
        except:
            raise serializers.ValidationError('id为{}的数据不存在'.format(id))
        return id

    def create(self, validated_data):
        #将摇纱领料的complete_return字段设置为True
        reeling_obj = Reeling.objects.get(id=validated_data['id'])
        reeling_obj.complete_return = True
        reeling_obj.save()
        #将与该领料单相连的回毛记录的complete_return也设置为True
        for return_obj in reeling_obj.reeling_return.all():
            return_obj.complete_return = True
            return_obj.save()
        return reeling_obj
