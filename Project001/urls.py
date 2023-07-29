"""Project001 URL Configuration

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
from apis import views
from apis.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup/', signup),
    path('users/login/', login),
    path('users/forgetpassword/', forget_password),
    path('contact/', contact_view, name='contact'),
    path('product_details/<str:product_id>/', product_details, name='product_details'),
    path('cart/<str:username>/', cart_view, name='cart'),
]
