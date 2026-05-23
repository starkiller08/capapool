from django.urls import path
from . import views

urlpatterns = [
	path('', views.candidate_list, name='candidate_list'),
	path('search/', views.candidate_search, name='candidate_search'),
	path('create/', views.create_candidate_profile, name='create_candidate_profile'),
	path('<int:candidate_id>/edit/', views.edit_candidate_profile, name='edit_candidate_profile'),
]