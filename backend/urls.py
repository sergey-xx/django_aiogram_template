from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('liveconfigs/', include('liveconfigs.urls'), name='liveconfigs'),
    path('api/', include('api.urls')),
]
