import csv
from django.core.management.base import BaseCommand

from stockapi.models import CompanyData


class Command(BaseCommand):
    help = 'Import data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CompanyData.objects.create(
                    name=row['Name'],
                    bse_code=row['BSE Code'],
                    nse_code=row['NSE Code'],
                    industry=row['Industry'],
                    current_price=self.to_decimal(row['Current Price']),
                    price_to_earning=self.to_decimal(row['Price to Earning'], 0.0),
                    market_capitalization=self.to_decimal(row['Market Capitalization']),
                    dividend_yield=self.to_decimal(row['Dividend yield']),
                    net_profit_latest_quarter=self.to_decimal(row['Net Profit latest quarter']),
                    yoy_quarterly_profit_growth=self.to_decimal(row.get('YOY Quarterly profit growth', None)),
                    debt_to_equity=self.to_decimal(row['Debt to equity'], 0.0),  # Default value for debt_to_equity
                    price_to_sales=self.to_decimal(row['Price to Sales']),
                    sales_growth=self.to_decimal(row['Sales growth'], 0.0),
                    eps=self.to_decimal(row['EPS']),
                    free_cash_generated_from_ebidta=self.to_decimal(row['Free Cash generated from EBIDTA']),
                    evebitda=self.to_decimal(row['EVEBITDA']),
                    price_to_book_value=self.to_decimal(row.get('Price to book value', None)),
                    ev_by_fcf=self.to_decimal(row['EV by FCF']),
                    merged_data=row['Merged_data'],
                    url=row['URL']
                )

    def to_decimal(self, value, default=None):
        try:
            return float(value) if value else default
        except ValueError:
            return default
