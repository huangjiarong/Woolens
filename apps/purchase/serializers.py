import copy

from rest_framework import serializers

from .models import PurchaseOrder, Purchase, TakeGoods
from warehouse_management.models import Inventory
from money_management.models import Due


class PurchaseOrderSerializers(serializers.ModelSerializer):
    """
    购货订单的Serializer类
    """
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def validate_number(self, number):
        if number <= 0:
            raise serializers.ValidationError('购货数量应大于0')
        return number

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError('购货单价应大于0')
        return price

    def validate_preorder_num(self, preorder_num):
        if preorder_num <= 0:
            raise serializers.ValidationError('可赊应大于0')
        return preorder_num

    def validate_preorder_price(self, preorder_price):
        if preorder_price <= 0:
            raise serializers.ValidationError('赊货单价应大于0')
        return preorder_price

    def create(self, validated_data):
        validated_data['total'] = validated_data['number'] * validated_data['price']
        validated_data['preorder_total'] = validated_data['preorder_num'] * validated_data['preorder_price']
        validated_data['tax_total'] = validated_data['tax_price'] * validated_data['number']
        validated_data['remain'] = validated_data['number']
        pur_order = PurchaseOrder.objects.create(**validated_data)
        #添加或修改一条应付款记录
        due_dict = {}
        due_dict['client'] = pur_order.supplier
        due_dict['source_ordNum'] = pur_order.ord_num
        due_dict['business_type'] = '购货订单'
        due, created = Due.objects.get_or_create(**due_dict)
        if created:
            due.ord_num = pur_order.ord_num
            due.date = pur_order.order_date
            due.money = pur_order.total
            due.not_cancel = pur_order.total
        else:
            due.money += pur_order.total
            due.not_cancel += pur_order.total

        due.save()
        return pur_order

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.woolens.name
        ret['client_name'] = instance.supplier.name
        ret['packaging'] = instance.woolens.packaging.id
        ret['packaging_name'] = instance.woolens.packaging.name
        ret['color_num'] = instance.woolens.color.color_num
        ret['color'] = instance.woolens.color.id
        ret['color_name'] = instance.woolens.color.color
        ret['batch_num'] = instance.woolens.batch_num
        ret['dyelot_num'] = instance.woolens.dyelot_num
        if instance.check_status:
            ret['check_status'] = '已审核'
        else:
            ret['check_status'] = '未审核'
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ('total', 'preorder_total', 'tax_total', 'check_status', 'complete_return', 'remain')



class PurchaseSerializers(serializers.ModelSerializer):
    """
    购货单的Serializer类
    """
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def create(self, validated_data):
        validated_data['total'] = validated_data['price'] * validated_data['number']
        validated_data['tax_total'] = validated_data['tax_price'] * validated_data['number']
        validated_data['sum'] = validated_data['total']
        purchase = Purchase.objects.create(**validated_data)

        #添加进库存
        dict = {}
        dict['name'] = purchase.woolens.name
        dict['packaging'] = purchase.woolens.packaging
        dict['color'] = purchase.woolens.color
        dict['dyelot_num'] = purchase.woolens.dyelot_num
        dict['batch_num'] = purchase.woolens.batch_num
        dict['warehouse'] = purchase.warehouse
        material, created = Inventory.objects.get_or_create(**dict)
        if created:
            material.woolens_type = '原材料'
            material.number = validated_data['number']
            material.assess_price = validated_data['price']
            material.actual_price = 0
        else:
            new_number = material.number + validated_data['number']
            material.assess_price = (material.assess_price * material.number +
                                     purchase.total) / new_number
            material.number = new_number
        material.save()

        #添加或修改一条应付款记录
        due_dict = {}
        due_dict['source_ordNum'] = purchase.ord_num
        due_dict['client'] = purchase.supplier
        due_dict['business_type'] = '购货'
        due, created = Due.objects.get_or_create(**due_dict)
        if created:
            due.ord_num = purchase.ord_num
            due.date = purchase.date
            due.money = purchase.total
            due.not_cancel = purchase.total
        else:
            due.money += purchase.total
            due.not_cancel += purchase.total

        due.save()
        return purchase

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.woolens.name
        ret['client_name'] = instance.supplier.name
        ret['warehouse_name'] = instance.warehouse.name
        ret['packaging_name'] = instance.woolens.packaging.name
        ret['color_name'] = instance.woolens.color.color
        ret['color_num'] = instance.woolens.color.color_num
        ret['batch_num'] = instance.woolens.batch_num
        ret['dyelot_num'] = instance.woolens.dyelot_num
        return ret

    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ('total', 'tax_total', 'sum')


class TakeGoodsListSerializers(serializers.ListSerializer):
    """
        TakeGoods的ListSerializer类, 序列化和反序列化多个TakeGoods时会用到
    """
    def validate(self, attrs):
        """
        attrs数据类型为[
        {purchase_order: [PurchaseOrderObject(1), PurchaseOrderObject(2)], take_num: 100, ...},
        {purchase_order: [PurchaseOrderObject(2), PurchaseOrderObject(3)], take_num: 200, ...}]
        ]
        1.深拷贝一份原数据以便用于返回，因为接下来的操作会修改到attrs原数据
        2.构造两个空列表存放对应的购货订单和数量, 再构造一个列表存放前两个列表的对应关系:
            goods_lst = [
            [PurchaseOrderObject(1), PurchaseOrderObject(2)],
            [PurchaseOrderObject(2), PurchaseOrderObject(3)]
            ]
            take_num_lst = [
            100, 200
            ]
            goods_takenum_lst = [
                [[PurchaseOrderObject(1), PurchaseOrderObject(2)], 100]
                [[PurchaseOrderObject(2), PurchaseOrderObject(3)], 200]
            ]
        3.用set找出本次请求一共有多少种购货订单,再转换为列表类型:
            set(
            PurchaseOrderObjects(1),PurchaseOrderObjects(2),PurchaseOrderObjects(3)
            )
            new_goods_lst = list(set(..))
        4.将goods_takenum_lst中的PurchaseOrderObjects对象都替换为new_goods_lst中的PurchaseOrderObjects对象,
        因为goods_takenum_lst中的PurchaseOrderObjects对象都不是同个对象,比如goods_takenum_lst[0][0]中的
        PurchaseOrderObjects(2)和goods_takenum_lst[1][0]中的PurchaseOrderObjects(2)不是同个对象,修改其中一个的
        remain字段并不会影响到另一个对象的remain, 经过4的操作后这两个对象将是同个对象
        5.模拟取货,遍历goods_takenum_lst, 对每个goods_take_num_lst[i][0]中的PurchaseOrderObjects对象,如果它的
        剩余数量remain大于取货数量goods_take_num_lst[i][1],则remain减去取货数量并将取货数量设为0,否则取货数量
        减去剩余数量并将剩余剩余设为0
        模拟取货通过的话最后的每个取货数量都为0, 如果不为0则说明模拟取货失败,验证不成功
        """
        new_attrs = copy.deepcopy(attrs)
        goods_lst, take_num_lst = [], []
        for pur_order in attrs:
            goods_lst.append(pur_order['purchase_order'])
            take_num_lst.append(pur_order['take_num'])
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


class TakeGoodsSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.complete_return:
            ret['complete_return'] = '已结束'
        else:
            ret['complete_return'] = '未结束'
        return ret

    def validate(self, attrs):
        total_num = 0
        for pur_order in attrs['purchase_order']:
            total_num += pur_order.remain
        if attrs['take_num'] > total_num:
            raise serializers.ValidationError('取货数量大于剩余数量')
        return attrs

    def validate_purchase_order(self, purchase_order):
        """
        重写purchase_order的验证,每条数据它们的订单和毛料需相同才可通过验证
        """
        ord_num_lst = []
        woolens_lst = []
        for pur_order in purchase_order:
            ord_num_lst.append(pur_order.ord_num)
            woolens_lst.append(pur_order.woolens)
        if (len(set(ord_num_lst)) != 1) or (len(set(woolens_lst)) != 1):
            raise serializers.ValidationError('所选数据的订单号和毛料需一致')
        return purchase_order

    def create(self, validated_data):
        #创建取货记录
        validated_data['ord_num'] = validated_data['purchase_order'][0].ord_num
        validated_data['name'] = validated_data['purchase_order'][0].woolens.name
        validated_data['packaging'] = validated_data['purchase_order'][0].woolens.packaging
        validated_data['color'] = validated_data['purchase_order'][0].woolens.color
        validated_data['dyelot_num'] = validated_data['purchase_order'][0].woolens.dyelot_num
        validated_data['batch_num'] = validated_data['purchase_order'][0].woolens.batch_num
        validated_data['take_total'] = validated_data['take_num'] * validated_data['take_price']
        pur_order_objs = validated_data.pop('purchase_order')
        take_goods = TakeGoods.objects.create(**validated_data)
        take_goods.purchase_order.add(*pur_order_objs)

        #已经创建完取货记录后，需要将对应购货订单里的数量进行减少
        take_num = validated_data['take_num']
        for pur_order in pur_order_objs:
            if take_num > pur_order.remain:
                take_num -= pur_order.remain
                pur_order.remain = 0
            else:
                pur_order.remain -= take_num
            pur_order.save()

        #添加进库存
        dict = {}
        dict['name'] = take_goods.name
        dict['packaging'] = take_goods.packaging
        dict['color'] = take_goods.color
        dict['dyelot_num'] = take_goods.dyelot_num
        dict['batch_num'] = take_goods.batch_num
        dict['warehouse'] = take_goods.warehouse
        material, created = Inventory.objects.get_or_create(**dict)
        if created:
            material.woolens_type = '原材料'
            material.number = validated_data['take_num']
            material.assess_price = take_goods.take_price
            material.actual_price = 0
        else:
            new_number = material.number + validated_data['take_num']
            material.assess_price = (material.assess_price * material.number +
                                               take_goods.take_total) / new_number
            material.number = new_number
        material.save()

        #取货后添加或修改一条应付款记录
        due_dict = {}
        due_dict['source_ordNum'] = take_goods.ord_num
        due_dict['client'] = pur_order_objs[0].supplier
        due_dict['business_type'] = '订货'
        due, created = Due.objects.get_or_create(**due_dict)
        if created:
            due.ord_num = take_goods.ord_num
            due.date = take_goods.take_date
            due.money = take_goods.take_total
            due.not_cancel = take_goods.take_total
        else:
            due.money += take_goods.take_total
            due.not_cancel += take_goods.take_total

        due.save()
        return take_goods

    class Meta:
        model = TakeGoods
        fields = '__all__'
        list_serializer_class = TakeGoodsListSerializers
        read_only_fields = ('complete_return', 'take_total', 'name', 'ord_num', 'packaging', 'color',
                            'dyelot_num', 'batch_num', 'take_total', 'complete_return')



class CompleteReturnPurchaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    index = serializers.IntegerField()

    def validate_id(self, id):
        try:
            purchase = PurchaseOrder.objects.get(id=id)
        except:
            raise serializers.ValidationError('id为{}的数据不存在'.format(id))
        return id

    def create(self, validated_data):
        #将购货订单的complete_return字段设置为True
        purchase_ord_obj = PurchaseOrder.objects.get(id=validated_data['id'])
        purchase_ord_obj.complete_return = True
        purchase_ord_obj.save()
        #将与该购货订单相连的取货记录的complete_return页设置为True
        for take_goods_obj in purchase_ord_obj.take_goods.all():
            take_goods_obj.complete_return = True
            take_goods_obj.save()
        return purchase_ord_obj