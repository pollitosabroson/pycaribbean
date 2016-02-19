from django.db import models

# Create your models here.


class Autor(models.Model):
    nombre = models.TextField(max_length=100)
    apellido = models.TextField(max_length=100)


class Libro(models.Model):
    nombre = models.TextField(max_length=100)
    editorial = models.TextField(max_length=100)
    genero = models.TextField(max_length=100)
    descripcion = models.TextField()
    autor = models.ForeignKey(
        Autor,
        null=True
    )

    def __unicode__(self):
        return self.editorial
