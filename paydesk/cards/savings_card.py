from ..models import *
from datetime import datetime

class SavingsCard():
    def __init__(self, card):
        self.card = card

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