from django.urls import path, include
from . import views

urlpatterns = [
    path('fitness/centre/register/', views.RegisterFitnessCentreAPI.as_view()),
    path('fitness/centre/', views.GetOwnerFitnessCentreAPI.as_view()),
    path('fitness/centre/membership/plan/create/', views.CreateMembershipPlan.as_view()),
    path('fitness/centre/membership/plan/<int:membership_id>/delete/', views.DeleteMembershipPlan.as_view()),
    path('fitness/centre/membership/plan/<int:membership_id>/update/', views.UpdateMembershipPlan.as_view()),
    path('fitness/centre/membership/plans/', views.CreateMembershipPlan.as_view()),
    path('fitness/centre/user/membership/start/', views.StartUserMembershipAPI.as_view()),
    path('fitness/centre/member/add/', views.AddMemberToFitnessCentreAPI.as_view()),
    path('fitness/centre/member/remove/', views.RemoveMemberFromFitnessCentreAPI.as_view()),
]
