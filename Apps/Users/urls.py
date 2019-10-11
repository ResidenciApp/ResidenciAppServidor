from django.urls import path, include
from .views import PeopleView, RoleView, OwnerView
from rest_framework import routers

"""
DefaultRouter: crear un enrutador dentro de la applicacion Users ('api/v1/users/')
para optener y guardar usuarios en el servidor
"""

router = routers.DefaultRouter()

# api/v1/users/people/
router.register('people', PeopleView, base_name='people')

# api/v1/users/role/
router.register('role', RoleView, base_name='role')

# api/v1/users/owner/
router.register('owner', OwnerView, base_name='owner')


urlpatterns = [
    # api/v1/users/
    path('', include(router.urls))
]
