from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'birthday', 'itn']
        labels = {
            'first_name': "Ім'я",
            'last_name': "Прізвище",
            'birthday': "Дата народження",
            'itn': "ІПН"
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'itn': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday > date.today():
            raise ValidationError('Дата не може бути в майбутньому.')
        return birthday

class AccountForm(forms.ModelForm):
    card_type = forms.ChoiceField(
        choices=[('', 'Не вибрано')] + Account.CARD_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип карти'
    )
    
    currency = forms.ChoiceField(
        choices=[('', 'Не вибрано')] + Account.CURRENCY_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Валюта'
    )
    
    class Meta:
        model = Account
        fields = ['card_type', 'card_number', 'pin', 'cvv', 'currency']
        labels = {
            'card_number': 'Номер карти',
            'pin': 'PIN',
            'cvv': 'CVV',
        }
        widgets = {
            'card_type': forms.Select(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'pin': forms.TextInput(attrs={'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if len(card_number) != 16:
            raise forms.ValidationError("Номер карти має бути 16 цифр.")
        return card_number

    def clean_pin(self):
        pin = self.cleaned_data['pin']
        if len(pin) != 4:
            raise forms.ValidationError("PIN код має бути 4 цифри.")
        return pin

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if len(cvv) != 3:
            raise forms.ValidationError("CVV має бути 3 цифри.")
        return cvv
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.registration_date = date.today()
        instance.valid_until = instance.registration_date + timedelta(days=4*365)
        
        # Зберігаємо об'єкт, якщо commit=True
        if commit:
            instance.save()
        return instance
    
class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['limit', 'interest_rate']
        widgets = {
            'limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'limit': 'Ліміт',
            'interest_rate': 'Відсоткова ставка',
        }

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount', 'interest_rate']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'amount': 'Сума',
            'interest_rate': 'Відсоткова ставка',
        }
        
class RegisterAdminForm(UserCreationForm):
    usable_password = None
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class LoginAdminForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))