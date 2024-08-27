from django.db import models


class CSVData(models.Model):
    data = models.JSONField()  # Storing the CSV data as JSON for easy retrieval and searching
    uploaded_at = models.DateTimeField(auto_now_add=True)  # To keep track of when the data was uploaded

    def __str__(self):
        return f"CSV Data uploaded on {self.uploaded_at}"


class UploadedCSV(models.Model):
    file_name = models.CharField(max_length=255)
    created_by = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CompanyData(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    bse_code = models.CharField(max_length=10, null=True, blank=True)
    nse_code = models.CharField(max_length=10, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_to_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    market_capitalization = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    net_profit_latest_quarter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yoy_quarterly_profit_growth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    debt_to_equity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_to_sales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sales_growth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    free_cash_generated_from_ebidta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    evebitda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_to_book_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ev_by_fcf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    merged_data = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)


