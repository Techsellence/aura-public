from django.contrib import admin
from .models import UploadedCSV


@admin.register(UploadedCSV)
class UploadedCSVAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'created_by', 'created_at')
    search_fields = ('file_name', 'created_by__username')
    list_filter = ('created_at',)
