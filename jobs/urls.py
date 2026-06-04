from django.urls import path
from . import views


urlpatterns = [
	path('', views.job_list, name='job_list'),
	path('search/', views.job_search, name='job_search'),
	path('create/', views.create_job, name='create_job'),
	path('my-jobs/', views.my_jobs, name='my_jobs'),
	path('<int:job_id>/edit/', views.edit_job, name='edit_job'),
]