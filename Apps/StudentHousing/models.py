from django.db import models
from Apps.Users.models import People

class ResidencePublication(models.Model):
    name = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    price = models.IntegerField()
    address = models.CharField(max_length=64)
    rules = models.CharField(max_length=1024)

    # TODO: Cuando Vladimir haya creado el modelo 'neighborhood' y 'locality'
    # de la App 'Location' Hacer las relaciones
    neighborhood = models.CharField(max_length=255)
    locality = models.CharField(max_length=16)

    # Hacer la relación ForeignKey con Owner de la App Users
    owner = models.CharField(max_length=255)


class Comment(models.Model):
    content = models.CharField(max_length=255)
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)


class Qualification(models.Model):
    number = models.IntegerField()
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)


class Service(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
