header = [
    {'title': 'Список осіб', 'currency': 'currency', 'back': 'index', 'main': 'index', 'update': 'persons', 'search': 'persons'},    # persons
    {'title': 'Список рахунків', 'currency': 'currency', 'back': 'index', 'main': 'index', 'update': 'accounts', 'search': 'accounts'},    # accounts
    {'title': 'Список операцій', 'currency': 'currency', 'back': 'index', 'main': 'index', 'update': 'operations'},    # operations
    {'title': 'Сторінка особи', 'currency': 'currency', 'back': 'persons', 'main': 'index'},    # person
    {'title': 'Сторінка рахунку', 'currency': 'currency', 'back': 'accounts', 'main': 'index'},    # account
    {'title': 'Створити особу', 'currency': 'currency', 'back': 'persons', 'main': 'index', 'update': 'create_person'},    # create_person
    {'title': 'Створити рахунок', 'currency': 'currency', 'back': 'accounts', 'main': 'index', 'update': 'create_account'},    # create_account
    {'title': 'Видача готівки', 'currency': 'currency', 'back': 'account', 'main': 'index', 'update': 'issuance_cash', 'type': 'account'},    # issuance_cash
    {'title': 'Поповнення рахунку', 'currency': 'currency', 'back': 'account', 'main': 'index', 'update': 'account_repl', 'type': 'account'},    # account_repl
    {'title': 'Переказ коштів', 'currency': 'currency', 'back': 'account', 'main': 'index', 'update': 'transfer_funds', 'type': 'account'},    # transfer_funds
    {'title': 'Оплата кредиту', 'currency': 'currency', 'back': 'account', 'main': 'index', 'update': 'pay_credit', 'type': 'account'},    # pay_credit
    {'title': 'Редагування даних особи', 'currency': 'currency', 'back': 'person', 'main': 'index', 'type': 'person'},    # edit_person
    {'title': 'Редагування даних рахунку', 'currency': 'currency', 'back': 'account', 'main': 'index', 'type': 'account'},    # edit_account
    {'title': 'Додати рахунок', 'currency': 'currency', 'back': 'person', 'main': 'index', 'type': 'person'},    # add_account
    {'title': 'Головна сторінка', 'currency': 'currency', 'main': 'index', 'update': 'index'},    # index
    {'title': 'Створити кредит'},    # create_credit
    {'title': 'Створити депозит'},    # create_deposit
    {'title': 'Стартова сторінка'},    # start
    {'title': 'Реєстрація', 'back': 'start'},    # register
    {'title': 'Вхід', 'back': 'start'},    # login
]

class HeaderMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        index = kwargs.get('index')
        context['header'] = header[index]
        return context