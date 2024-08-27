from rest_framework import serializers


class CSVFileSerializer(serializers.Serializer):
    file = serializers.FileField()
