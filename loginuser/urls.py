"""auth URL Configuration

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

from django.urls import path, include
from .views import  login_user, logout_user, register_user, verifyotp
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('', login_user, name="login"),
    path('login_user', login_user, name="login"),
    path('logout_user', logout_user, name='logout'),
    path('register_user', register_user, name='register_user'),
    path('verifyotp', verifyotp, name='verifyotp'),
    path('verifyotp/<id>', verifyotp, name='verifyotp'),
    #path('test/', testview, name='testview'),
    path('api/schema/', SpectacularAPIView.as_view(), name = 'api-schema'),
    path('api/docs/',
    SpectacularSwaggerView.as_view(url_name = 'api-schema') , name = 'api-docs')


]
