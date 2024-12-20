from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.urls import reverse

class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birthday = models.DateField()
    itn = models.CharField(max_length=10, unique=True)
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )
        
    def clean(self):
        if self.birthday > date.today():
            raise ValidationError('Дата не можу бути в майбутньому.')
    
    def get_absolute_url(self):
        return reverse("person", kwargs={"pk": self.pk})
    
    
class Account(models.Model):
    CARD_TYPES = [
        ('UNIVERSAL', 'Універсальна'),
        ('DEBIT', 'Дебетова'),
        ('CREDIT', 'Кредитна'),
        ('SAVINGS', 'Ощадна')
    ]
    
    CURRENCY_TYPES = [
        ('USD', 'Долар США'),
        ('EUR', 'Євро'),
        ('UAN', 'Гривня')
    ]
    
    card_type = models.CharField(max_length=16, choices=CARD_TYPES)
    card_number = models.CharField(max_length=16, unique=True)
    pin = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)
    amount = models.FloatField(default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_TYPES)
    registration_date = models.DateField()
    valid_until = models.DateField()
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse("account", kwargs={"pk": self.pk})

class Operation(models.Model):
    OPERATION_TYPES = [
        ('TRANSFER', 'Переказ коштів'),
        ('CASH_WITHDRAWAL', 'Видача готівки'),
        ('RECHARGE', 'Поповнення рахунку'),
        ('CREDIT_PAYMENT', 'Оплата кредиту')
    ]
    
    operation_type = models.CharField(max_length=16, choices=OPERATION_TYPES)
    operation_datetime = models.DateTimeField()
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_operations')
    recipient_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='received_operations')
    sender_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sent_operations')
    recipient_person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, related_name='received_operations')
    amount = models.FloatField()
    
class Credit(models.Model):
    limit = models.FloatField()
    dept = models.FloatField(default=0)
    interest_rate = models.FloatField()
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='credit')
    
class Deposit(models.Model):
    amount = models.FloatField()
    interest_rate = models.FloatField()
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='deposit')