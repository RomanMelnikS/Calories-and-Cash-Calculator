import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_date = dt.date.today()
        today_stats = sum(
            day.amount for day in self.records if day.date == today_date)
        return today_stats

    def get_week_stats(self):
        today_date = dt.date.today()
        week_delta = dt.timedelta(days=7)
        first_date = today_date - week_delta
        week_stats = sum(
            day.amount for day in self.records
            if first_date < day.date <= today_date)
        return week_stats


class CashCalculator(Calculator):

    USD_RATE = 80.0
    EURO_RATE = 90.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()

        currency_basis = {'rub': {'rate': self.RUB_RATE, 'name': 'руб'},
                          'usd': {'rate': self.USD_RATE, 'name': 'USD'},
                          'eur': {'rate': self.EURO_RATE, 'name': 'Euro'}
        }

        remains = self.limit - today_stats

        if currency not in currency_basis:
            return (f'Ошибка. Данной валюты нет в валютной базе.')

        rate = currency_basis[currency]['rate']
        name = currency_basis[currency]['name']

        currency_remains = remains / rate

        if remains > 0:
            return (f'На сегодня осталось {currency_remains:.2f} '
                    f'{name}')
        if remains < 0:
            currency_remains = abs(currency_remains)
            return (f'Денег нет, держись: твой долг '
                    f'- {currency_remains:.2f} '
                    f'{name}')

        return f'Денег нет, держись'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            remains_calory = self.limit - today_stats
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remains_calory} кКал')
        return f'Хватит есть!'


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.date = date
        self.comment = comment

        if self.date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(
                self.date, self.DATE_FORMAT).date()
