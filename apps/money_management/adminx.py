import xadmin

from .models import Payment, Receipt, Due, Account_Due, Payment_to_Due, Receipt_to_AccountDue


class DueAdmin:
    list_display = ['ord_num', 'source_ordNum', 'client', 'business_type', 'date', 'money',
                    'had_cancel', 'not_cancel']


class PaymentAdmin:
    list_display = ['ord_num', 'due', 'client', 'date', 'pay_money', 'settlement_num', ]



class PayToDueAdmin:
    list_display = ['payment', 'due', 'cancel']


class ReceiptAdmin:
    list_display = ['ord_num', 'account_due', 'client', 'date', 'receipt_money', 'settlement_num']


class AccountDueAdmin:
    list_display = ['ord_num', 'source_ordNum', 'client', 'business_type', 'date', 'money',
                    'had_cancel', 'not_cancel']


class ReceiptToAccountDueAdmin:
    list_display = ['receipt', 'account_due', 'cancel']


xadmin.site.register(Payment, PaymentAdmin)
xadmin.site.register(Receipt, ReceiptAdmin)
xadmin.site.register(Due, DueAdmin)
xadmin.site.register(Account_Due, AccountDueAdmin)
xadmin.site.register(Payment_to_Due, PayToDueAdmin)
xadmin.site.register(Receipt_to_AccountDue, ReceiptToAccountDueAdmin)
