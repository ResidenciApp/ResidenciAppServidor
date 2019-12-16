from django.db import models
from Apps.Users.models import People
from Apps.Users.models import Owner


class Service(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    address = models.CharField(max_length=64)


class ResidencePublication(models.Model):
    name = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    price = models.IntegerField()
    rules = models.CharField(max_length=1024)
    description = models.CharField(max_length=2048, null=True, blank=True)
    owner = models.ForeignKey(Owner, null=False, blank=False, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    location = models.OneToOneField(Location, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(max_length=255)
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)


class Qualification(models.Model):
    number = models.IntegerField()
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)


class Notification(models.Model):
    description = models.CharField(max_length=255)
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)

class Report(models.Model):
    reportType = models.CharField(max_length=255) #No se si este sea el tipo de Reporte
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)


class Message(models.Model):
    content = models.CharField(max_length=255)
    transmitter = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE,related_name="message_transmitter")
    receiver = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE, related_name="message_receiver")

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)

class AverageView(models.Model):
    description = models.CharField(max_length=255)
