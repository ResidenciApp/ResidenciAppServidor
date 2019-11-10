from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from Apps.Users.models import *
# Create your views here.

class ResidencePublicationView(viewsets.ModelViewSet):
    queryset = ResidencePublication.objects.all()
    serializer_class = ResidencePublicationSerializers

    def create(self, request):
        data = request.data

        # request.data: Tiene el siguiente diccionario de datos
    # {
    #   "idResidence" : "",
    #   "name" : "",
    #   "photo": 1,
    #   "value": "",
    #   "address": "",
    #   "rules": 1,
    #   "neighborhood": 1,
    #   "locality": 1,
    #   "owner": 1
    # }

       #neighborhood = Neighborhood.objects.get(id=request.data.get('idNeighborhood'))
        owner=Owner.objects.get(id=request.data.get('owner'))
        #locality = Locality.objects.get(id=request.data.get('locality'))

        residence = ResidencePublication(
            name=request.data.get('residenceName'),
            photo=request.data.get('photo'),
            value=request.data.get('value'),
            address=request.data.get('address'),
            owner=owner,
            #neighborhood = heighborhood,
            #locality = locality
        )

        residence.save()

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class QualificationView(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializers

class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers

class ReportView(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializers

class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers

class PromotionView(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializers