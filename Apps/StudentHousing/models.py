from django.db import models

from Apps.Users.models import Owner
class ResidencePublication(models.Model):
    name = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    price = models.IntegerField()
    address = models.CharField(max_length=64)
    rules = models.CharField(max_length=1024)
    neighborhood = models.CharField(max_length=255)
    locality = models.CharField(max_length=16)
    owner = models.ForeignKey(Owner, null=False, blank=False, on_delete=models.CASCADE)


from Apps.Users.models import People
class Comment(models.Model):
    content = models.CharField(max_length=255)
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)

from Apps.Users.models import People
class Qualification(models.Model):
    number = models.IntegerField()
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(People, null=False, blank=False, on_delete=models.CASCADE)

class Service(models.Model):
    number = models.IntegerField()
    description = rules = models.CharField(max_length=1024)
    publication = models.ForeignKey(ResidencePublication, null=False, blank=False, on_delete=models.CASCADE)