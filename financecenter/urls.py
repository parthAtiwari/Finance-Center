import asyncio
"""financecenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.fchome,name='home'),
    path('auth/',include('authuser.urls')),
    path('stockmarket/',include('stockmarket.urls')),
    path('my-finance/',include('myfinance.urls')),
    path('profile/',views.display_profile,name='display_profile'),
    path('dashboard/',views.user_dashboard,name='user_dashboard'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('developer-contact/',views.developer_contact,name='developer-contact')

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)