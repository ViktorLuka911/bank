class CurrencyConversion:
    def __init__(self, from_currency, to_currency, rate):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate

# Список конверсій валют
conversions = [
    CurrencyConversion("UAH", "UAH", 1.0),
    CurrencyConversion("UAH", "USD", 0.027),
    CurrencyConversion("UAH", "EUR", 0.025),
    CurrencyConversion("USD", "UAH", 37.037),
    CurrencyConversion("USD", "USD", 1.0),
    CurrencyConversion("USD", "EUR", 0.926),
    CurrencyConversion("EUR", "UAH", 40.0),
    CurrencyConversion("EUR", "USD", 1.081),
    CurrencyConversion("EUR", "EUR", 1.0)
]

# Функція для переведення валют
def convert_currency(amount, from_currency, to_currency):
    for conversion in conversions:
        if conversion.from_currency == from_currency and conversion.to_currency == to_currency:
            return amount * conversion.rate
    raise ValueError(f"Конверсія з {from_currency} в {to_currency} не знайдена!")