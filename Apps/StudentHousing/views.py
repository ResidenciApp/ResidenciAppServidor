from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
# Create your views here.

class ResidencePublicationView(viewsets.ModelViewSet):
    queryset = ResidencePublication.objects.all()
    serializer_class = ResidencePublicationSerializers

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class QualificationView(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializers

class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers
