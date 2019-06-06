import json

from rest_framework import serializers

from .models import Due, Payment, Payment_to_Due, Account_Due, Receipt, Receipt_to_AccountDue


#应付款的序列化类
class DueSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    index = serializers.CharField(write_only=True, default=' ')
    cancel = serializers.FloatField(write_only=True, default=0)
    id = serializers.IntegerField()

    class Meta:
        model = Due
        fields = '__all__'


#付款单的序列化类
class PaymentSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    due = DueSerializer(many=True, write_only=True)

    def validate(self, attrs):
        all_cancel = 0
        for d in attrs['due']:
            all_cancel += d['cancel']
        if attrs['pay_money'] != all_cancel:
            raise serializers.ValidationError('支付金额和总核销金额应相等')
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['account_name'] = instance.account.name
        ret['client_name'] = instance.client.name
        ret['settlement_type_name'] = instance.settlement_type.name
        ret['due'] = []
        payment_to_due_objs = Payment_to_Due.objects.filter(payment=instance)
        for payment_to_due in payment_to_due_objs:
            payment_to_due.due.__dict__['client'] = payment_to_due.due.client.id
            serializers = DueSerializer(data=payment_to_due.due.__dict__)
            if serializers.is_valid(raise_exception=False):
                data_dict = dict(serializers.data)
                data_dict['cancel'] = payment_to_due.cancel
                ret['due'].append(data_dict)
        return ret

    def create(self, validated_data):
        due_objs = validated_data.pop('due')
        #创建付款单
        payment = Payment.objects.create(**validated_data)

        for due_obj in due_objs:
            #修改应付款的已核销和未核销
            due = Due.objects.get(id=due_obj['id'])
            due.had_cancel += due_obj['cancel']
            due.not_cancel -= due_obj['cancel']
            due.save()
            #创建付款单和应付款之间的多对多关系
            payment_to_due = Payment_to_Due.objects.create(payment=payment, due=due, cancel=due_obj['cancel'])

        return payment

    class Meta:
        model = Payment
        fields = '__all__'


#应收款的序列化类
class AccountDueSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    index = serializers.CharField(write_only=True, default=' ')
    cancel = serializers.FloatField(write_only=True, default=0)
    id = serializers.IntegerField()

    class Meta:
        model = Account_Due
        fields = '__all__'


#收款单的序列化类
class ReceiptSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    account_due = AccountDueSerializer(many=True, write_only=True)

    def validate(self, attrs):
        all_cancel = 0
        for d in attrs['account_due']:
            all_cancel += d['cancel']
        if attrs['receipt_money'] != all_cancel:
            raise serializers.ValidationError('收款金额和本次核销总额应相等')
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['account_name'] = instance.account.name
        ret['client_name'] = instance.client.name
        ret['settlement_type_name'] = instance.settlement_type.name
        ret['account_due'] = []
        receipt_to_accountDue_objs = Receipt_to_AccountDue.objects.filter(receipt=instance)
        for receipt_to_accountDue in receipt_to_accountDue_objs:
            receipt_to_accountDue.account_due.__dict__['client'] = receipt_to_accountDue.account_due.client.id
            serializers = AccountDueSerializer(data=receipt_to_accountDue.account_due.__dict__)
            if serializers.is_valid(raise_exception=False):
                data_dict = dict(serializers.data)
                data_dict['cancel'] = receipt_to_accountDue.cancel
                ret['account_due'].append(data_dict)
        return ret

    def create(self, validated_data):
        account_due_objs = validated_data.pop('account_due')
        #创建收款单
        receipt = Receipt.objects.create(**validated_data)

        for account_due_obj in account_due_objs:
            #修改应收款的已核销和未核销
            account_due = Account_Due.objects.get(id=account_due_obj['id'])
            account_due.had_cancel += account_due_obj['cancel']
            account_due.not_cancel -= account_due_obj['cancel']
            account_due.save()
            #创建收款单和应收款之间的多对多关系
            receipt_to_accountDue = Receipt_to_AccountDue.objects.create(receipt=receipt,
                    account_due=account_due, cancel=account_due_obj['cancel'])

        return receipt

    class Meta:
        model = Receipt
        fields = '__all__'
