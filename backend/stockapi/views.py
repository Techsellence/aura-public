import csv
import json
import math

import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CSVData, UploadedCSV, CompanyData
from .utils.screener_query_utils import (
    get_url_suffix, get_full_url,
    check_gourab_cookie,
    check_gourab_csrftoken,
    check_for_lapsed_cookie,
    get_data_as_dataframe,
    download_to_merged,
    clean_BSE,
    generate_url,
    get_screener_query_mcap_file
)


class UploadCSV(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        data = [row for row in reader]

        # Store CSV data
        csv_data = CSVData(data=json.dumps(data))
        csv_data.save()

        # Store file upload information
        uploaded_csv = UploadedCSV(
            file_name=file.name,
            created_by='Sohini M',
        )
        uploaded_csv.save()

        return Response({"status": "success", "data": data})


class SearchCSV(APIView):

    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get('keyword', '').lower()
        csv_data = CSVData.objects.last()  # Get the last uploaded CSV data
        if not csv_data:
            return Response({"status": "error", "message": "No CSV data available"}, status=404)

        data = json.loads(csv_data.data)
        filtered_data = [row for row in data if any(keyword in str(value).lower() for value in row.values())]

        if not filtered_data:
            return Response({"status": "success", "data": [], "message": "No matching results found"}, status=200)

        return Response({"status": "success", "data": filtered_data}, status=200)


def contains_nan(instance):
    for field in instance._meta.get_fields():
        value = getattr(instance, field.name)
        if isinstance(value, float) and math.isnan(value):
            return True
    return False


class FetchScreenerQueryData(APIView):

    def post(self, request, *args, **kwargs):
        low = request.data.get('low', 0)
        high = request.data.get('high', 80000000)

        # API endpoint URL
        url_suffix = get_url_suffix(low, high)
        url = get_full_url(url_suffix, url_name="raw_query")

        # Headers and data payload as per your cURL request
        headers = {
            'cookie': check_gourab_cookie(),
            'referer': url_suffix,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        data = {
            'csrfmiddlewaretoken': check_gourab_csrftoken()
        }

        # Check if the cookie has lapsed
        print(f"URL: {url}")
        # Make the request
        response = requests.post(url, headers=headers, data=data)

        soup = BeautifulSoup(response.text, 'html.parser')
        cookie_did_not_lapse = check_for_lapsed_cookie(soup)
        if not cookie_did_not_lapse:
            return Response({'error': 'Cookie has lapsed, please update the tokens'}, status=400)

        # Check if the request was successful
        if response.status_code == 200:
            df = get_data_as_dataframe(response)
            df = download_to_merged(df)
            df = clean_BSE(df)
            df['URL'] = df['Merged_data'].apply(generate_url)
            df = df.fillna(0)

            # Delete existing entries in the CompanyData table
            CompanyData.objects.all().delete()

            # Save the new data into the CompanyData table
            company_data_objects = [
                CompanyData(
                    name=row.get('Name'),
                    bse_code=row.get('BSE Code'),
                    nse_code=row.get('NSE Code'),
                    industry=row.get('Industry'),
                    current_price=row.get('Current Price'),
                    price_to_earning=row.get('Price to Earning'),
                    market_capitalization=row.get('Market Capitalization'),
                    dividend_yield=row.get('Dividend yield'),
                    net_profit_latest_quarter=row.get('Net Profit latest quarter'),
                    yoy_quarterly_profit_growth=row.get('YOY Quarterly profit growth'),
                    debt_to_equity=row.get('Debt to equity'),
                    price_to_sales=row.get('Price to Sales'),
                    sales_growth=row.get('Sales growth'),
                    eps=row.get('EPS'),
                    free_cash_generated_from_ebidta=row.get('Free Cash generated from EBIDTA'),
                    evebitda=row.get('EVEBITDA'),
                    price_to_book_value=row.get('Price to book value'),
                    ev_by_fcf=row.get('EV by FCF'),
                    merged_data=row.get('Merged_data'),
                    url=row.get('URL')
                )
                for _, row in df.iterrows()
            ]
            # Convert the data to JSON format
            company_data_json = [
                {
                    "name": obj.name,
                    "bse_code": obj.bse_code,
                    "nse_code": obj.nse_code,
                    "industry": obj.industry,
                    "current_price": float(obj.current_price) if obj.current_price else None,
                    "price_to_earning": float(obj.price_to_earning) if obj.price_to_earning else None,
                    "market_capitalization": float(obj.market_capitalization) if obj.market_capitalization else None,
                    "dividend_yield": float(obj.dividend_yield) if obj.dividend_yield else None,
                    "net_profit_latest_quarter": float(
                        obj.net_profit_latest_quarter) if obj.net_profit_latest_quarter else None,
                    "yoy_quarterly_profit_growth": float(
                        obj.yoy_quarterly_profit_growth) if obj.yoy_quarterly_profit_growth else None,
                    "debt_to_equity": float(obj.debt_to_equity) if obj.debt_to_equity else None,
                    "price_to_sales": float(obj.price_to_sales) if obj.price_to_sales else None,
                    "sales_growth": float(obj.sales_growth) if obj.sales_growth else None,
                    "eps": float(obj.eps) if obj.eps else None,
                    "free_cash_generated_from_ebidta": float(
                        obj.free_cash_generated_from_ebidta) if obj.free_cash_generated_from_ebidta else None,
                    "evebitda": float(obj.evebitda) if obj.evebitda else None,
                    "price_to_book_value": float(obj.price_to_book_value) if obj.price_to_book_value else None,
                    "ev_by_fcf": float(obj.ev_by_fcf) if obj.ev_by_fcf else None,
                    "merged_data": obj.merged_data,
                    "url": obj.url,
                }
                for obj in company_data_objects
            ]

            # Print the data as JSON
            print(json.dumps(company_data_json, indent=4))

            # Save the new data into the CompanyData table
            CompanyData.objects.bulk_create(company_data_objects)

            return Response({'message': 'Data retrieved, saved, and printed as JSON successfully'}, status=200)
        else:
            return Response({'error': f'Failed to retrieve data: Status code {response.status_code}'},
                            status=response.status_code)
