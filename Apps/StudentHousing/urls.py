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

# api/v1/users/notification/
router.register('notification', NotificationView, base_name='notification')

# api/v1/users/message/
router.register('message', MessageView, base_name='message')

# api/v1/users/report/
router.register('report', ReportView, base_name='report')

# api/v1/users/promotion/
router.register('promotion', PromotionView, base_name='promotion')

# api/v1/users/upload-photo-residence/
router.register('upload-photo-residence', UploadPhotoView, base_name='upload-photo-residence')

urlpatterns = [
    # api/v1/users/
    path('search', Search.as_view()),
    path('', include(router.urls))
]