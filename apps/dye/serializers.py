import copy

from rest_framework import serializers

from .models import Dye, DyeNotice, DyeReturn
from money_management.models import Due
from warehouse_management.models import Inventory


class DyeListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        """
        attrs数据类型为[
            {reeling: InventoryObjects(1), take_num: 100, ...},
            {reeling: InventoryObjects(2), take_num: 200, ...},
            {reeling: InventoryObjects(1), take_num: 50, ...},
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
        for dye in attrs:
            goods_lst.append(dye['reeling'])
            take_num_lst.append(dye['number'])

        for goods_takenum in zip(goods_lst, take_num_lst):
            if goods_takenum[0] not in goods_takenum_map.keys():
                goods_takenum_map[goods_takenum[0]] = goods_takenum[1]
            else:
                goods_takenum_map[goods_takenum[0]] += goods_takenum[1]

        for goods, take_num in goods_takenum_map.items():
            if goods.number < take_num:
                raise serializers.ValidationError('总的领料数量大于库存')
        return attrs


class DyeSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.reeling.name
        ret['packaging_name'] = instance.reeling.packaging.name
        ret['color_name'] = instance.reeling.color.color
        ret['color_num'] = instance.reeling.color.color_num
        ret['dyelot_num'] = instance.reeling.dyelot_num
        ret['batch_num'] = instance.reeling.batch_num
        ret['process_name'] = instance.process.name
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    def validate(self, attrs):
        if attrs['number'] > attrs['reeling'].number:
            raise serializers.ValidationError('领料数量大于库存量')
        return attrs

    def create(self, validated_data):
        validated_data['remain'] = validated_data['number']
        validated_data['total_price'] = validated_data['number'] * validated_data['price']
        dye = Dye.objects.create(**validated_data)
        #创建染色领料后需减少相应的库存
        reeling_obj = validated_data['reeling']
        reeling_obj.number -= validated_data['number']
        reeling_obj.save()
        return dye

    class Meta:
        model = Dye
        list_serializer_class = DyeListSerializer
        fields = '__all__'
        read_only_fields = ('remain', 'total_price', 'complete_return')


class DyeNoticeListSerializers(serializers.ListSerializer):
    def validate(self, attrs):
        """
            同purchase.serializer的TakeGoodsListSerializer的注释
        """
        new_attrs = copy.deepcopy(attrs)
        goods_lst, take_num_lst = [], []
        for pur_order in attrs:
            goods_lst.append(pur_order['dye'])
            take_num_lst.append(pur_order['number'])
        goods_takenum_lst = []
        for i in range(len(goods_lst)):
            goods_takenum_lst.append([goods_lst[i], take_num_lst[i]])

        #获取该次请求操作的所有购货订单
        goods_set = set()
        for i in goods_lst:
            for j in i:
                goods_set.add(j)
        new_goods_lst = list(goods_set)

        #将goods_takenum_lst中值相等的PurchaseOrder对象都替换为相同的对象
        for i in range(len(goods_takenum_lst)):
            for j in range(len(goods_takenum_lst[i][0])):
                goods_takenum_lst[i][0][j] = new_goods_lst[new_goods_lst.index(goods_takenum_lst[i][0][j])]

        #模拟取货,对相应的购货订单的剩余数量进行减少
        for index, goods_takenum in enumerate(goods_takenum_lst):
            for goods in goods_takenum[0]:
                if goods.remain <= goods_takenum_lst[index][1]:
                    goods_takenum_lst[index][1] -= goods.remain
                    goods.remain = 0
                else:
                    goods.remain -= goods_takenum_lst[index][1]
                    goods_takenum_lst[index][1] = 0

        for goods_takenum in goods_takenum_lst:
            if goods_takenum[1] > 0:
                raise serializers.ValidationError('总的取货数量大于剩余量')
        return new_attrs


class DyeNoticeSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    def validate(self, attrs):
        total_number = 0
        for dye_obj in attrs['dye']:
            total_number += dye_obj.remain
        if attrs['number'] > total_number:
            raise serializers.ValidationError('数量大于领料数量')
        return attrs

    def validate_dye(self, dye):
        """
        重写dye的验证,只允许批量选取订单号及毛料一样的数据,如:
        [{'dye':1, 'ord_num':'110'}, {'dye':1, 'ord_num':'110'}]正确
        [{'dye':2, 'ord_num':'110'}, {'dye':1, 'ord_num':'110'}]错误
        """
        reeling_lst, ord_num_lst = [], []
        for dye_obj in dye:
            reeling_lst.append(dye_obj.reeling)
            ord_num_lst.append(dye_obj.ord_num)
        if (len(set(reeling_lst))) != 1 or (len(set(ord_num_lst))) != 1:
            raise serializers.ValidationError('所选数据的订单号和毛料需一致')
        return dye

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['get_dye_color'] = str(instance.dye_color.id) + ',' + instance.dye_color.color_num
        ret['ord_num'] = instance.ord_num
        ret['name'] = instance.name
        ret['packaging_name'] = instance.packaging.name
        ret['color_name'] = instance.color.color
        ret['color_num'] = instance.color.color_num
        ret['dyelot_num'] = instance.dyelot_num
        ret['batch_num'] = instance.batch_num
        ret['dye_color_num'] = instance.dye_color.color_num
        ret['dye_color_name'] = instance.dye_color.color
        ret['process_name'] = instance.dye.first().process.name
        ret['process'] = instance.dye.first().process.id
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    def create(self, validated_data):
        validated_data['ord_num'] = validated_data['dye'][0].ord_num
        validated_data['name'] = validated_data['dye'][0].reeling.name
        validated_data['packaging'] = validated_data['dye'][0].reeling.packaging
        validated_data['color'] = validated_data['dye'][0].reeling.color
        validated_data['dyelot_num'] = validated_data['dye'][0].reeling.dyelot_num
        validated_data['batch_num'] = validated_data['dye'][0].reeling.batch_num
        dye_objs = validated_data.pop('dye')
        dye_notice = DyeNotice.objects.create(**validated_data)
        dye_notice.dye.add(*dye_objs)
        #创建了染色通知后，需要将相连的染色领料单的数量减少
        number = validated_data['number']
        for dye in dye_objs:
            if number > dye.remain:
                number -= dye.remain
                dye.remain = 0
            else:
                dye.remain -= number
            dye.save()
        return dye_notice

    class Meta:
        model = DyeNotice
        fields = '__all__'
        list_serializer_class = DyeNoticeListSerializers
        read_only_fields = ('ord_num', 'name', 'packaging', 'color', 'dyelot_num', 'batch_num',
                            'complete_return', )


class DyeReturnSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['packaging'] = instance.packaging.name
        ret['color'] = instance.color.color
        ret['color_num'] = instance.color.color_num
        ret['process_name'] = instance.dye_notice.first().dye.first().process.name
        ret['color_name'] = instance.color.color
        ret['packaging_name'] = instance.packaging.name
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    def validate_dye_notice(self, dye_notice):
        """
        重写dye_notice的验证,它们的ord_num, name, packaging, color, dyelot_num,
        batch_num, dye_color需一致才可通过验证
        """
        all = []
        ord_num_lst, name_lst, packaging_lst, color_lst, dyelot_num_lst, \
        batch_num_lst, dye_color_lst= (
            [], [], [], [], [], [], []
        )
        for r in dye_notice:
            ord_num_lst.append(r.ord_num)
            name_lst.append(r.name)
            packaging_lst.append(r.packaging)
            color_lst.append(r.color)
            batch_num_lst.append(r.batch_num)
            dyelot_num_lst.append(r.dyelot_num)
            dye_color_lst.append(r.dye_color)
        all.append(ord_num_lst)
        all.append(name_lst)
        all.append(packaging_lst)
        all.append(color_lst)
        all.append(dyelot_num_lst)
        all.append(batch_num_lst)
        all.append(dye_color_lst)
        for tmp in all:
            if len(set(tmp)) != 1:
                raise serializers.ValidationError('所选数据的订单号和毛料需一致')
        return dye_notice

    def create(self, validated_data):
        #创建回毛记录
        validated_data['ord_num'] = validated_data['dye_notice'][0].ord_num
        validated_data['color'] = validated_data['dye_notice'][0].dye_color
        validated_data['batch_num'] = validated_data['dye_notice'][0].batch_num
        validated_data['name'] = validated_data['dye_notice'][0].name
        validated_data['packaging'] = validated_data['dye_notice'][0].packaging
        validated_data['total'] = validated_data['price'] * validated_data['number']
        validated_data['process_total'] = validated_data['process_price'] * validated_data['number']
        validated_data['total_price'] = validated_data['total'] + validated_data['process_total']
        validated_data['assess_price'] = validated_data['price']
        dye_notice_objs = validated_data.pop('dye_notice')
        dye_return = DyeReturn.objects.create(**validated_data)
        dye_return.dye_notice.add(*dye_notice_objs)

        #添加染色产品进仓库
        data = {}
        data['name'] = dye_return.name
        data['color'] = dye_return.color
        data['packaging'] = dye_return.packaging
        data['batch_num'] = dye_return.batch_num
        data['dyelot_num'] = dye_return.dyelot_num
        data['warehouse'] = dye_return.warehouse
        inventory, created = Inventory.objects.get_or_create(**data)
        if not created:
            inventory.assess_price = (validated_data['total_price'] + inventory.number * inventory.assess_price) / (
                    validated_data['number'] + inventory.number)
            inventory.number += validated_data['number']
        else:
            inventory.woolens_type = '染色产品'
            inventory.number = validated_data['number']
            inventory.assess_price = validated_data['process_price'] + validated_data['price']
        inventory.save()

        #取货完后需要新增或修改一条应付款记录
        due_dict = {}
        due_dict['source_ordNum'] = dye_return.ord_num
        due_dict['client'] = dye_notice_objs[0].dye.first().process
        due_dict['business_type'] = '染色'
        due, created = Due.objects.get_or_create(**due_dict)
        if created:
            due.ord_num = dye_return.ord_num
            due.date = dye_return.return_date
            due.money = dye_return.total_price
            due.not_cancel = dye_return.total_price
        else:
            due.money += dye_return.total_price
            due.not_cancel += dye_return.total_price
        due.save()

        return dye_return


    class Meta:
        model = DyeReturn
        fields = '__all__'
        read_only_fields = ('ord_num', 'name', 'packaging', 'color', 'batch_num', 'total',
                            'process_total', 'total_price', 'assess_price', 'actual_price',
                            'A', 'A1', 'complete_return', )


class CompleteReturnDyeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    index = serializers.IntegerField()

    def validate_id(self, id):
        try:
            dye = Dye.objects.get(id=id)
        except:
            raise serializers.ValidationError('id为{}的数据不存在'.format(id))
        return id

    def create(self, validated_data):
        #将染色领料的complete_return字段设置为True
        dye_obj = Dye.objects.get(id=validated_data['id'])
        dye_obj.complete_return = True
        dye_obj.save()
        #将与该染色单相连的染色通知单的complete_return也设置为True
        for dyeNotice_obj in dye_obj.dye_notice.all():
            dyeNotice_obj.complete_return = True
            dyeNotice_obj.save()
            #将与该染色通知单相连的回毛记录的complete_return设置为True
            for dyeReturn_obj in dyeNotice_obj.dye_return.all():
                dyeReturn_obj.complete_return = True
                dyeReturn_obj.save()
        return dye_obj
