from django.urls import path
from . import views

urlpatterns = [
	path('', views.candidate_list, name='candidate_list'),
	path('search/', views.candidate_search, name='candidate_search'),
]