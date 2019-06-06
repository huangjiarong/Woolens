from rest_framework import serializers

from .models import Sale, SaleOrder, SaleExport
from money_management.models import Account_Due, Receipt_to_AccountDue, Receipt


#销售单的ListSerializer类
class SaleListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        """
        attrs数据类型为[
            {woolens: InventoryObjects(1), take_num: 100, ...},
            {woolens: InventoryObjects(2), take_num: 200, ...},
            {woolens: InventoryObjects(1), take_num: 50, ...},
        ]
        1.构造两个空列表存放对应的库存对象和取货数量:
            woolens_lst = [
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
        woolens_lst, take_num_lst = [], []
        for sale in attrs:
            woolens_lst.append(sale['woolens'])
            take_num_lst.append(sale['sale_num'])

        for goods_takenum in zip(woolens_lst, take_num_lst):
            if goods_takenum[0] not in goods_takenum_map.keys():
                goods_takenum_map[goods_takenum[0]] = goods_takenum[1]
            else:
                goods_takenum_map[goods_takenum[0]] += goods_takenum[1]

        for goods, take_num in goods_takenum_map.items():
            if goods.number < take_num:
                raise serializers.ValidationError('总的销售数量大于库存')
        return attrs


#销售单的序列化类
class SaleSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def validate(self, attrs):
        if attrs['sale_num'] > attrs['woolens'].number:
            raise serializers.ValidationError('销售数量大于库存量')
        attrs['sale_total'] = attrs['sale_num'] * attrs['sale_price']
        attrs['tax_total'] = attrs['sale_num'] * attrs['tax_price']
        attrs['book_total'] = attrs['book_num'] * attrs['book_price']
        attrs['count'] = attrs['sale_total'] + attrs['tax_total']
        if attrs['count'] < attrs['proceeds']:
            raise serializers.ValidationError('本次收款数额大于应收款数额')
        attrs['arrear'] =  attrs['count'] - attrs['proceeds']
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.woolens.name
        ret['packaging_name'] = instance.woolens.packaging.name
        ret['color_name'] = instance.woolens.color.color
        ret['color_num'] = instance.woolens.color.color_num
        ret['batch_num'] = instance.woolens.batch_num
        ret['dyelot_num'] = instance.woolens.dyelot_num
        ret['client_name'] = instance.client.name
        ret['account_name'] = instance.account.name
        ret['warehouse_name'] = instance.woolens.warehouse.name
        return ret

    def create(self, validated_data):
        sale = Sale.objects.create(**validated_data)
        #创建销售单后减去库存的数量
        sale.woolens.number -= sale.sale_num
        sale.woolens.save()
        #创建销售单后增加或修改一条应收款记录
        account_due_dict = {}
        account_due_dict['source_ordNum'] = sale.ord_num
        account_due_dict['client'] = sale.client
        account_due_dict['business_type'] = '销货应收款'
        account_due, created = Account_Due.objects.get_or_create(**account_due_dict)
        if created:
            account_due.ord_num = sale.ord_num
            account_due.date = sale.ord_date
        account_due.money += sale.count
        account_due.had_cancel += sale.proceeds
        account_due.not_cancel += sale.arrear
        account_due.client.receivable += sale.arrear

        account_due.client.save()
        account_due.save()
        return sale

    class Meta:
        model = Sale
        fields = '__all__'
        list_serializer_class = SaleListSerializer
        read_only_fields = ('sale_total', 'book_total', 'tax_total', 'arrear', 'count', )


#销售订单的序列化类
class SaleOrderSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def validate(self, attrs):
        if attrs['sale_num'] > attrs['woolens'].number:
            raise serializers.ValidationError('销售数量大于库存量')
        attrs['sale_total'] = attrs['sale_num'] * attrs['sale_price']
        attrs['book_total'] = attrs['book_num'] * attrs['book_price']
        attrs['tax_total'] = attrs['sale_num'] * attrs['tax_price']
        attrs['remain'] = attrs['sale_num']
        attrs['count'] = attrs['tax_total'] + attrs['sale_total']
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.woolens.name
        ret['packaging_name'] = instance.woolens.packaging.name
        ret['color_name'] = instance.woolens.color.color
        ret['color_num'] = instance.woolens.color.color_num
        ret['batch_num'] = instance.woolens.batch_num
        ret['dyelot_num'] = instance.woolens.dyelot_num
        ret['client_name'] = instance.client.name
        ret['warehouse_name'] = instance.woolens.warehouse.name
        return ret

    def create(self, validated_data):
        saleOrder = SaleOrder.objects.create(**validated_data)
        #创建销售订单后增加客户的预付款
        saleOrder.client.pre_receivable += saleOrder.proceeds
        saleOrder.client.save()

        return saleOrder

    class Meta:
        model = SaleOrder
        fields = '__all__'
        list_serializer_class = SaleListSerializer  #此处销售订单可用销售单的ListSerializer类
        read_only_fields = ('sale_total', 'book_total', 'tax_total', 'remain','count',)


#销售出货单的ListSerializer类
class SaleExportListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        """
        attrs数据类型为[
            {sale_order: SaleOrderObjects(1), take_num: 100, ...},
            {sale_order: SaleOrderObjects(2), take_num: 200, ...},
            {sale_order: SaleOrderObjects(1), take_num: 50, ...},
        ]
        1.构造两个空列表存放对应的库存对象和取货数量:
            sale_order_lst = [
                SaleOrderObjects(1),SaleOrderObjects(2), SaleOrderObjects(1)
            ]
            take_num_lst = [
                100, 200, 50
            ]
        2.构建一个dict, 结构为:goods_takenum_map = {
            SaleOrderObjects(1): 150, SaleOrderObjects(2): 100
        }
        3.遍历dict, 对take_num和库存的remain进行比较即可
        """
        goods_takenum_map = {}
        sale_order_lst, take_num_lst = [], []
        for sale in attrs:
            sale_order_lst.append(sale['sale_order'])
            take_num_lst.append(sale['take_num'])

        for goods_takenum in zip(sale_order_lst, take_num_lst):
            if goods_takenum[0] not in goods_takenum_map.keys():
                goods_takenum_map[goods_takenum[0]] = goods_takenum[1]
            else:
                goods_takenum_map[goods_takenum[0]] += goods_takenum[1]

        for goods, take_num in goods_takenum_map.items():
            if goods.remain < take_num:
                raise serializers.ValidationError('总的销售数量大于剩余数量')
        return attrs


#销售出货的序列化类
class SaleExportSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    def validate(self, attrs):
        if attrs['take_num'] > attrs['sale_order'].remain:
            raise serializers.ValidationError('取货数量大于剩余数量')

        attrs['take_total'] = attrs['take_num'] * attrs['take_price']
        attrs['ord_num'] = attrs['sale_order'].ord_num
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = instance.sale_order.woolens.name
        return ret

    def create(self, validated_data):
        sale_export = SaleExport.objects.create(**validated_data)
        #创建出货单后需要减少库存的数量
        sale_export.sale_order.woolens.number -= sale_export.take_num
        sale_export.sale_order.woolens.save()
        #创建出货单后需要减少订单的剩余数量
        sale_export.sale_order.remain -= sale_export.take_num
        sale_export.sale_order.save()
        #创建出货单后添加或修改一条应收款记录
        account_due_dict = {}
        account_due_dict['source_ordNum'] = sale_export.ord_num
        account_due_dict['client'] = sale_export.sale_order.client
        account_due_dict['business_type'] = '销货出货应收款'
        account_due, created = Account_Due.objects.get_or_create(**account_due_dict)
        if created:
            account_due.ord_num = sale_export.ord_num
            account_due.date = sale_export.ord_date
        account_due.money += sale_export.take_total
        #如果账户的预付款大于等于本次应付款的金额, 则从预付款中减去, 修改应付款的已核销
        #否则将预付款清空, 修改应付款的未核销和已核销
        if account_due.client.pre_receivable >= sale_export.take_total:
            account_due.client.pre_receivable -= sale_export.take_total
            account_due.had_cancel += sale_export.take_total
        else:
            account_due.had_cancel += account_due.client.pre_receivable
            account_due.not_cancel += (sale_export.take_total - account_due.client.pre_receivable)
            account_due.client.pre_receivable = 0
            account_due.client.receivable += account_due.not_cancel

        account_due.client.save()
        account_due.save()
        return sale_export

    class Meta:
        model = SaleExport
        fields = '__all__'
        list_serializer_class = SaleExportListSerializer
        read_only_fields = ('take_total', 'ord_num')
