from rest_framework import serializers
from .models import Prestamo

# Serializer for reading prestamos (with nested details)
class PrestamoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'