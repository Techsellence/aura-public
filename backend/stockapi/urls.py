from django.urls import path
from .views import UploadCSV, SearchCSV, FetchScreenerQueryData


urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload-csv'),
    path('search/', SearchCSV.as_view(), name='search-csv'),
    path('fetch-screener-query-data/', FetchScreenerQueryData.as_view(), name='fetch_screener_query_data'),

]
