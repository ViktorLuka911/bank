from ..models import *
from datetime import datetime
from .currency_convertion import convert_currency

class CreditCard():
    def __init__(self, card, credit):
        self.card = card
        self.credit = credit

    def issuance_cash(self, amount):
                        
        self.credit.dept += amount
        self.credit.save()

        Operation.objects.create(
            operation_type='Видача готівки',
            operation_datetime=datetime.now(),
            sender_account=self.card,
            sender_person=self.card.person,
            recipient_person=None,
            recipient_account=None,
            amount=amount
        )
        
    def pay_credit(self, amount):
        
        self.credit.dept += amount
        self.credit.save()

        Operation.objects.create(
            operation_type='Оплата кредиту',
            operation_datetime=datetime.now(),
            sender_account=self.card,
            sender_person=self.card.person,
            recipient_person=None,
            recipient_account=None,
            amount=amount
        )
        
    def transfer_funds(self, amount, recipient):
                 
        Operation.objects.create(
            operation_type='Переказ коштів',
            operation_datetime=datetime.now(),
            sender_account=self.card,
            sender_person=self.card.person,
            recipient_person=recipient.person,
            recipient_account=recipient,
            amount=amount
        )
               
        self.credit.dept += amount
        self.credit.save()
        
        amount = convert_currency(amount, self.card.currency, recipient.currency)
        
        if recipient.card_type == "CREDIT":
            credit = Credit.objects.get(account=recipient)
            credit.dept -= amount
            credit.save()
        else:
            recipient.amount += amount
            recipient.save()
        

        
        