from django.contrib import admin
from django.urls import path, include
import request.views as request

urlpatterns = [
    path('success/url/',request.file_download),
    # path('admin/', admin.site.urls),
    path('', include('request.urls')),
]
