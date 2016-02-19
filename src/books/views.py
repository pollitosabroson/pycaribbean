from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Libro, Autor
from .serializers import (
    LibroSerializer, AutorSerializer,
    InfoLibroSerializer)


class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Libro.objects.all().order_by('id')
        serializer = InfoLibroSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        libro = get_object_or_404(Libro, id=pk)
        serializer = InfoLibroSerializer(libro)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            libro = get_object_or_404(Libro, id=pk)
            serializer.update(
                instance=libro, validated_data=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorViewSet(viewsets.ModelViewSet):

    serializer_class = AutorSerializer
    queryset = Autor.objects.all()
