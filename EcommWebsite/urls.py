"""EcommWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.views.csrf import csrf_failure
from . import views

handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'

admin.site.site_header = "Shop N Blog Admin"
admin.site.site_title = "Shop N Blog Admin Panel"
admin.site.index_title = "Welcome to Shop N Blog Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shopping.urls')),
    path('home/', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('', views.index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


