from rest_framework import serializers
from .models import GpxFile

class GpxFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpxFile
        fields = '__all__'
        read_only_fields = ('created_at')