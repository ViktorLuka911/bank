from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import *
from .cards import *
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .utils import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

class StartView(HeaderMixin, TemplateView):
    template_name = 'paydesk/start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=17)
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(HeaderMixin, CreateView):
    form_class = RegisterAdminForm
    template_name = 'paydesk/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=18)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class LoginUser(HeaderMixin, LoginView):
    form_class = LoginAdminForm
    template_name = 'paydesk/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=19)
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')

def logout_user(request):
    logout(request)
    return redirect('login')

class UserMainView(HeaderMixin, TemplateView):
    template_name = 'paydesk/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=14)
        return dict(list(context.items()) + list(c_def.items()))

class PersonsView(HeaderMixin, ListView):
    paginate_by = 5
    model = Person
    template_name = 'paydesk/persons.html'
    context_object_name = 'persons'
    
    def get_queryset(self):
        request = self.request
        search_query = request.GET.get('search', '')
        return Person.objects.filter(last_name__icontains=search_query) if search_query else Person.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        c_def = self.get_user_context(index=0)
        return dict(list(context.items()) + list(c_def.items()))
    
class AccountsView(HeaderMixin, ListView):
    paginate_by = 5
    model = Account
    template_name = 'paydesk/accounts.html'
    context_object_name = 'accounts'
    
    def get_queryset(self):
        request = self.request
        search_query = request.GET.get('search', '')
        return Account.objects.filter(person__isnull=False, card_number__icontains=search_query) if search_query else Account.objects.filter(person__isnull=False)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        c_def = self.get_user_context(index=1)
        return dict(list(context.items()) + list(c_def.items())) 

class OperationsView(HeaderMixin, ListView):
    paginate_by = 5
    model = Operation
    template_name = 'paydesk/operations.html'
    context_object_name = 'operations'
    
    def get_queryset(self):
        return Operation.objects.all().order_by('-operation_datetime')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=2)
        return dict(list(context.items()) + list(c_def.items()))

class AddAccountView(HeaderMixin, ListView):
    paginate_by = 5
    model = Account
    template_name = 'paydesk/add_account.html'
    context_object_name = 'accounts'
    
    def get_queryset(self):
        return Account.objects.filter(person__isnull=True)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['person'] = Person.objects.get(id=pk)
        c_def = self.get_user_context(index=13)
        return dict(list(context.items()) + list(c_def.items()))
        
class ConfirmAddAccountView(RedirectView):
    permanent = False
    pattern_name = 'person'
    
    def get_redirect_url(self, *args, **kwargs):
        person_id = kwargs['person_id']
        account_id = kwargs['account_id']
        
        account = Account.objects.get(id=account_id)
        account.person_id = person_id
        account.save()
        
        messages.success(self.request, "Рахунок успішно додано!")
        
        person = Person.objects.get(id=person_id)
        return person.get_absolute_url()

class PersonView(HeaderMixin, DetailView):
    model = Person
    template_name = 'paydesk/person.html'
    context_object_name = 'person'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['accounts'] = Account.objects.filter(person_id=pk)
        c_def = self.get_user_context(index=3)
        return dict(list(context.items()) + list(c_def.items()))

class AccountView(HeaderMixin, DetailView):
    paginate_by = 5
    model = Account
    template_name = 'paydesk/account.html'
    context_object_name = 'account'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        account = self.object
        context['operations'] = Operation.objects.filter(
            Q(sender_account=account) | Q(recipient_account=account)
        ).order_by('-operation_datetime')
        context['person'] = account.person
        context['accounts'] = Account.objects.filter(person_id=account.id)
        c_def = self.get_user_context(index=4)
        context['credit'] = Credit.objects.filter(account=account).first()
        context['deposit'] = Deposit.objects.filter(account=account).first()
        return dict(list(context.items()) + list(c_def.items()))

class CreatePersonView(HeaderMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'paydesk/create_person.html'
    success_url = reverse_lazy('persons')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Особу успішно створено!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=5)
        return dict(list(context.items()) + list(c_def.items()))
    
class UpdatePersonView(HeaderMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'paydesk/create_person.html'
    context_object_name = 'person'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        person = form.instance
        messages.success(self.request, "Особу успішно оновлено!")
        return HttpResponseRedirect(person.get_absolute_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=11)
        return dict(list(context.items()) + list(c_def.items()))
    
class CreateAccountView(HeaderMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'paydesk/create_account.html'
    
    def form_valid(self, form):
        new_account = form.save()
        
        if new_account.card_type == "SAVINGS":
            return redirect('create_deposit', pk=new_account.id)
        elif new_account.card_type in ["CREDIT", "UNIVERSAL"]:
            return redirect('create_credit', pk=new_account.id)
        else:
            messages.success(self.request, "Рахунок успішно створено!")
            return redirect('accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=6)
        return dict(list(context.items()) + list(c_def.items()))

class UpdateAccountView(HeaderMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'paydesk/create_account.html'
    context_object_name = 'account'

    def form_valid(self, form):
        account = form.save()
        messages.success(self.request, "Дані рахунку успішно оновлено!")
        return account.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = header[12]
        return context

class CreateCreditView(HeaderMixin, CreateView):
    model = Credit
    form_class = CreditForm
    template_name = 'paydesk/create_credit.html'
    
    def get_success_url(self):
        return self.object.account.get_absolute_url()
    
    def form_valid(self, form):
        account = Account.objects.get(id=self.kwargs['pk'])
        credit = form.save(commit=False)
        credit.account = account
        credit.save()
        
        messages.success(self.request, "Рахунок та кредит успішно створено!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, "Будь ласка, виправте помилки у формі.")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=15)
        return dict(list(context.items()) + list(c_def.items()))

class CreateDepositView(HeaderMixin, CreateView):
    model = Deposit
    form_class = DepositForm
    template_name = 'paydesk/create_deposit.html'
    
    def get_success_url(self):
        return self.object.account.get_absolute_url()
    
    def form_valid(self, form):
        account = Account.objects.get(id=self.kwargs['pk'])
        deposit = form.save(commit=False)
        deposit.account = account
        deposit.save()
        
        messages.success(self.request, "Рахунок та депозит успішно створено!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, "Будь ласка, виправте помилки у формі.")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(index=16)
        return dict(list(context.items()) + list(c_def.items()))

class DeletePersonView(DeleteView):
    model = Person
    success_url = reverse_lazy('persons')
    
    def get(self, request, *args, **kwargs):
        messages.success(self.request, "Особу успішно видалено!")
        return self.delete(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

class DeleteAccountView(DeleteView):
    model = Account
    success_url = reverse_lazy('accounts')

    def get(self, request, *args, **kwargs):
        messages.success(request, "Рахунок успішно видалено!")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

def card_factory(card, credit):
    if card.card_type == "SAVINGS":
        return SavingsCard(card)
    elif card.card_type == "UNIVERSAL":
        return UniversalCard(card, credit)
    elif card.card_type == "CREDIT":
        return CreditCard(card, credit)
    else:
        return DebitCard(card)

class IssuanceCashView(HeaderMixin, View):
    def get_credit_available(self, account):
        credit = Credit.objects.filter(account=account).first()
        if credit:
            return credit.limit - credit.dept
        return None

    def post(self, request, pk):
        account = Account.objects.get(id=pk)
        credit_available = self.get_credit_available(account)

        amount_operation = request.POST.get('amount_operation', '')

        if amount_operation:
            try:
                amount_operation = float(amount_operation)

                credit = Credit.objects.filter(account=account).first()
                if credit is None and account.amount < amount_operation:
                    messages.success(request, "Недостатньо коштів на рахунку!")
                    context = {
                        'account': account,
                        'credit_available': credit_available,
                        'header': header[7]
                    }
                    return render(request, 'paydesk/issuance_cash.html', context)
                elif credit is not None and credit_available < amount_operation:
                    messages.success(request, "Недостатньо коштів на рахунку!")
                    return render(request, 'paydesk/issuance_cash.html', {
                        'account': account,
                        'credit_available': credit_available,
                        'header': header[7]
                    })
                
                card = card_factory(account, credit)

                if account.card_type == 'UNIVERSAL':
                    choose = request.POST.get('choose')
                    card.issuance_cash(amount_operation, choose)
                else:
                    card.issuance_cash(amount_operation)

                messages.success(request, "Кошти успішно видано!")
                return redirect(account.get_absolute_url())

            except ValueError:
                messages.success(request, "Неправильне введення!")
                return render(request, 'paydesk/issuance_cash.html', {
                    'account': account,
                    'credit_available': credit_available,
                    'header': header[7]
                })

        return render(request, 'paydesk/issuance_cash.html', {
            'account': account,
            'credit_available': credit_available,
            'header': header[7]
        })

    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        credit_available = self.get_credit_available(account)
        return render(request, 'paydesk/issuance_cash.html', {
            'account': account,
            'credit_available': credit_available,
            'header': header[7]
        })

class AccountReplView(HeaderMixin, View):
    def post(self, request, pk):
        account = Account.objects.get(id=pk)
        amount_operation = request.POST.get('amount_operation', '')

        if amount_operation:
            try:
                amount_operation = float(amount_operation)

                credit = Credit.objects.filter(account=account).first()
                card = card_factory(account, credit)

                card.account_repl(amount_operation)
                messages.success(request, "Рахунок успішно поповнено!")
                return redirect(account.get_absolute_url())

            except ValueError:
                messages.success(request, "Неправильне введення!")
                return render(request, 'paydesk/account_repl.html', {
                    'account': account,
                    'header': header[8]
                })

        return render(request, 'paydesk/account_repl.html', {
            'account': account,
            'header': header[8]
        })

    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        return render(request, 'paydesk/account_repl.html', {
            'account': account,
            'header': header[8]
        })

class TransferFundsView(HeaderMixin, View):
    def get_credit_available(self, account):
        credit = Credit.objects.filter(account=account).first()
        if credit:
            return credit.limit - credit.dept
        return None

    def post(self, request, pk):
        account = Account.objects.get(id=pk)
        credit_available = self.get_credit_available(account)
        amount_operation = request.POST.get('amount_operation', '')
        recipient_card = request.POST.get('recipient_card', '')

        if amount_operation and recipient_card:
            try:
                amount_operation = float(amount_operation)
                
                recipient_account = Account.objects.get(card_number=recipient_card)
                
                credit = Credit.objects.filter(account=account).first()
                if credit is None and account.amount < amount_operation:
                    return render(request, 'paydesk/transfer_funds.html', {
                        'error': "Недостатньо коштів на рахунку",
                        'account': account,
                        'credit_available': credit_available,
                        'header': header[9]
                    })
                elif credit is not None and credit_available < amount_operation:
                    return render(request, 'paydesk/transfer_funds.html', {
                        'error': "Недостатньо коштів на рахунку",
                        'account': account,
                        'credit_available': credit_available,
                        'header': header[9]
                    })
                
                card = card_factory(account, credit)
                
                recipient_credit = Credit.objects.get(account=recipient_account)
                
                if (recipient_credit.limit - recipient_credit.dept) + amount_operation > recipient_credit.limit:
                    messages.success(request, "Перевищено нарахування доступних кредитних коштів!")
                    return render(request, 'paydesk/transfer_funds.html', {
                        'account': account,
                        'credit_available': credit_available,
                        'header': header[7]
                    })
                
                if account.card_type == 'UNIVERSAL':
                    choose = request.POST.get('choose')
                    card.transfer_funds(amount_operation, recipient_account, choose)
                else:
                    card.transfer_funds(amount_operation, recipient_account)

                messages.success(request, "Переказ коштів успішно проведено!")
                return redirect(account.get_absolute_url())

            except ValueError:
                messages.success(request, "Неправильне введення!")
                return render(request, 'paydesk/transfer_funds.html', {
                    'account': account,
                    'credit_available': credit_available,
                    'header': header[9]
                })
            except Account.DoesNotExist:
                messages.success(request, "Рахунок отримувача не знайдено!")
                return render(request, 'paydesk/transfer_funds.html', {
                    'account': account,
                    'credit_available': credit_available,
                    'header': header[9]
                })

        return render(request, 'paydesk/transfer_funds.html', {
            'account': account,
            'credit_available': credit_available,
            'header': header[9]
        })

    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        credit_available = self.get_credit_available(account)
        return render(request, 'paydesk/transfer_funds.html', {
            'account': account,
            'credit_available': credit_available,
            'header': header[9]
        })
        
class PayCreditView(HeaderMixin, View):
    def get_credit_available(self, account, credit):
        if credit:
            return credit.limit - credit.dept
        return None

    def post(self, request, pk):
        account = Account.objects.get(id=pk)
        credit = Credit.objects.filter(account=account).first()
        credit_available = self.get_credit_available(account, credit)
        amount_operation = request.POST.get('amount_operation', '')

        if amount_operation:
            try:
                amount_operation = float(amount_operation)
                
                if credit_available + amount_operation > credit.limit:
                    messages.success(request, "Перевищено нарахування доступних кредитних коштів!")
                    return render(request, 'paydesk/pay_credit.html', {
                        'account': account,
                        'credit_available': credit_available,
                        'header': header[7]
                    })

                card = card_factory(account, credit)

                card.pay_credit(amount_operation)

                messages.success(request, "Кредит успішно оплачено!")
                return redirect(account.get_absolute_url())

            except ValueError:
                messages.success(request, "Неправильне введення!")
                return render(request, 'paydesk/pay_credit.html', {
                    'account': account,
                    'credit_available': credit_available,
                    'header': header[10]
                })

        return render(request, 'paydesk/pay_credit.html', {
            'account': account,
            'credit_available': credit_available,
            'header': header[10]
        })

    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        credit = Credit.objects.filter(account=account).first()
        credit_available = self.get_credit_available(account, credit)
        return render(request, 'paydesk/pay_credit.html', {
            'account': account,
            'credit_available': credit_available,
            'header': header[10]
        })