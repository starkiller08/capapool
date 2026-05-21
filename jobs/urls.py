from django.urls import path
from . import views


urlpatterns = [
	path('', views.job_list, name='job_list'),
	path('search/', views.job_search, name='job_search'),
]