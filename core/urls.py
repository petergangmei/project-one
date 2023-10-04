
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('projectone.urls', 'projectone'), namespace='projectone')),
    path('ac/', include(('account.urls', 'account'), namespace='account')),
    path('api/',include(('api.urls', 'api'), namespace='api')),
]
