from django.urls import path

from .views import post_payment

urlpatterns = [
    path('payment/',
         post_payment,
         name='payment'), ]
