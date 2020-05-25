"""evillage URL Configuration

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

from app_0 import views

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('request/rationCard', views.req_ration_card_view, name='ration_card'),
    path('request/nativity', views.req_nativity_view, name='nativity'),
    path('request/income', views.req_income_view, name='income'),
    path('request/identityCard', views.req_identity_card_view, name='identity'),
    path('request/cast', views.req_cast_view, name='caste'),
    path('request/payTax', views.req_tax_view, name='pay_tax'),
    path('request/complaint', views.req_complaint_view, name='complaint'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:status>/<int:pk>/', views.detail_approval, name='dashboard-detail'),
]
