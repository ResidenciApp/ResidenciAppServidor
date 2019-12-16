from rest_framework import serializers
from .models import *


class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('__all__')

class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('__all__')


class ResidencePublicationSerializers(serializers.ModelSerializer):

    services = ServiceSerializers(read_only=True, many=True)
    location = LocationSerializers(read_only=True)

    class Meta:
        model = ResidencePublication
        fields = ('__all__')

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')

class QualificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Qualification

        fields = ('__all__')

class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('__all__')

class ReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('__all__')

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')

class PromotionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('__all__')

class AverageView(serializers.ModelSerializer):
    class Meta:
        model = AverageView
        fields = ('__all__')

