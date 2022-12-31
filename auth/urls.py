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
from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterAPI, VerifyOTP, DashboardView, load_bikes, UserOrders, UserCompleteOrders, ProtectedAPIView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.authtoken.views import ObtainAuthToken



urlpatterns = [
    path('', include('loginuser.urls')),
    path('api/protected/', ProtectedAPIView.as_view(), name='protected'),
    path('api/token-auth/', ObtainAuthToken.as_view(), name='auth_token'),
    path('register/', RegisterAPI.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('orders/', UserOrders.as_view(), name='orders'),
    path('orderscomplete/', UserCompleteOrders.as_view(), name ='orderscomplete'),
    path('admin/', admin.site.urls),
    #path('dash', customer_page, name='home'),
    path('dashboard/', DashboardView, name='dashboard'),
    path('ajax/load-bikes', load_bikes, name='ajax_load_bikes'),
    path('qrcode/', include('qrcodeweb.urls'), name = 'qrcode'),
        
    #path('ajax/load-bikes2', load_bikes2, name='ajax_load_bikes2'), 

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



