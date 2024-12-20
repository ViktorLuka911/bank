from ..models import *
from datetime import datetime
from .currency_convertion import convert_currency

class DebitCard():
    def __init__(self, card):
        self.card = card

    def issuance_cash(self, amount):
                        
        self.card.amount -= amount
        self.card.save()

        Operation.objects.create(
            operation_type='Видача готівки',
            operation_datetime=datetime.now(),
            sender_account=self.card,
            sender_person=self.card.person,
            recipient_person=None,
            recipient_account=None,
            amount=amount
        )
        
    def account_repl(self, amount):
                        
        self.card.amount += amount
        self.card.save()

        Operation.objects.create(
            operation_type='Поповнення рахунку',
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
        
        self.card.amount -= amount
        self.card.save()
        
        amount = convert_currency(amount, self.card.currency, recipient.currency)
                
        if recipient.card_type == 'CREDIT':
            credit = Credit.objects.get(account=recipient)
            credit.dept -= amount
            credit.save()
        else:
            recipient.amount += amount
            recipient.save()