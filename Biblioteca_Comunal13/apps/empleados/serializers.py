from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Empleado

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # para que no se vea al leer
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # sacamos la contraseña plana
        empleado = Empleado(**validated_data)
        empleado.password = make_password(password)  # la convertimos a hash
        empleado.save()
        return empleado

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = make_password(password)  # hash si se actualiza
        instance.save()
        return instance