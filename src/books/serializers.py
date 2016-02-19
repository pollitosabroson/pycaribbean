from rest_framework import serializers
from .models import Libro, Autor


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ('id', 'nombre', 'apellido',)


class LibroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Libro
        fields = (
            'id', 'nombre', 'descripcion', 'editorial', 'genero', 'autor',)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get(
            'descripcion', instance.descripcion)
        instance.editorial = validated_data.get(
            'editorial', instance.editorial)
        instance.genero = validated_data.get('genero', instance.genero)
        instance.autor_id = validated_data.get('autor', instance.autor_id)
        instance.save()


class InfoLibroSerializer(serializers.ModelSerializer):
    autor = serializers.CharField(
        source='autor.nombre'
    )

    class Meta:
        model = Libro
        fields = (
            'id', 'nombre', 'descripcion',
            'editorial', 'genero', 'autor',)
