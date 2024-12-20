from django.urls import path
from .views import *

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('main/', UserMainView.as_view(), name='index'),
    path('persons/', PersonsView.as_view(), name='persons'),
    path('accounts/', AccountsView.as_view(), name='accounts'),
    path('operations/', OperationsView.as_view(), name='operations'),
    path('persons/<int:pk>/', PersonView.as_view(), name='person'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    path('create_person/', CreatePersonView.as_view(), name='create_person'),
    path('create_account/', CreateAccountView.as_view(), name='create_account'),
    path('add_account/<int:pk>/', AddAccountView.as_view(), name='add_account'),
    path('confirm_add_account/<int:person_id>/<int:account_id>', ConfirmAddAccountView.as_view(), name='confirm_add_account'),
    
    path('delete_person/<int:pk>/', DeletePersonView.as_view(), name='delete_person'),
    path('delete_account/<int:pk>/', DeleteAccountView.as_view(), name='delete_account'),
    
    path('create_person/<int:pk>/', UpdatePersonView.as_view(), name='edit_person'),
    path('create_account/<int:pk>/', UpdateAccountView.as_view(), name='edit_account'),
    
    path('issuance_cash/<int:pk>/', IssuanceCashView.as_view(), name='issuance_cash'),
    path('account_repl/<int:pk>/', AccountReplView.as_view(), name='account_repl'),
    path('transfer_funds/<int:pk>/', TransferFundsView.as_view(), name='transfer_funds'),
    path('pay_credit/<int:pk>/', PayCreditView.as_view(), name='pay_credit'),
    
    path('create_credit/<int:pk>/', CreateCreditView.as_view(), name='create_credit'),
    path('create_deposit/<int:pk>/', CreateDepositView.as_view(), name='create_deposit')
]
