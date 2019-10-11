from django.contrib import admin
from .models import People, Role, Owner

admin.site.register(People)
admin.site.register(Role)
admin.site.register(Owner)