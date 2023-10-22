"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler403, handler404, handler500

urlpatterns = [
    path('admin/defender/', include('defender.urls')), # defender admin
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/', include('accounts.urls')),
    path("convert/", include("guest_user.urls")),
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

from app.views import error_404, error_403, error_500
handler404 = error_404
handler403 = error_403
handler500 = error_500

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
