from django.urls import path, include
from . import views

urlpatterns = [
    path('body-parts/', views.GetBodyPartsAPI.as_view()),
    path('body-part/<int:body_part_id>/excercises/', views.GetBodyPartExcercisesAPI.as_view()),
]
