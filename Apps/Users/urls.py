from django.urls import path, include
from .views import PeopleView, RoleView, OwnerView, TokenView, UserView
from rest_framework import routers


# DefaultRouter: crear un enrutador dentro de la applicacion Users ('api/v1/users/')
# para optener y guardar usuarios en el servidor


router = routers.DefaultRouter()

# api/v1/users/people/
router.register('people', PeopleView, base_name='people')

# api/v1/users/role/
router.register('role', RoleView, base_name='role')

# api/v1/users/owner/
router.register('owner', OwnerView, base_name='owner')

# api/v1/users/user/
router.register('user', UserView, base_name='user')

# api/v1/users/api-token-auth/
router.register('api-token-auth', TokenView, base_name='api-token-auth')


urlpatterns = [
    # api/v1/users/
    path('', include(router.urls))
]
