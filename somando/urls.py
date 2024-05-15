"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

app_name = 'somando'

urlpatterns = [
    path('', views.top, name='top'),
    path('experiences', views.experiences, name='experiences'),
    path('products', views.products, name='products'),
    path('products/<slug:url>', views.product, name='product'),
    path('contact', views.contact, name='contact'),
    path('contact/login', views.contactLogin, name='contactLogin'),
    path('contact/chat/<slug:id>', views.contactChat, name='contactChat'),
    path('privacy-policy', views.privacyPolicy, name='privacy-policy'),
    path('terms-of-use', views.termsOfUse, name='terms-of-use'),
    
    # redirect
    path('product/<slug:url>', views.productRedirect),
]
