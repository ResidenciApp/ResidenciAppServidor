from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# api/v1/users/residencePublication/
router.register('residence_publication', ResidencePublicationView, base_name='residencePublication')

# api/v1/users/comment/
router.register('comment', CommentView, base_name='comment')

# api/v1/users/qualification/
router.register('qualification', QualificationView, base_name='qualification')

# api/v1/users/service/
router.register('service', ServiceView, base_name='service')

urlpatterns = [
    # api/v1/users/
    path('', include(router.urls))
]