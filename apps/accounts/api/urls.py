from django.urls import path, include
from . import views

urlpatterns = [
    path('user/register/', views.RegisterApi_v3.as_view()),
    path('user/profile/', views.UserProfileAPI.as_view()),
    path('user/phone/exist/', views.PhoneNumberExistanceAPI.as_view()),
]
