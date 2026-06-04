from django.urls import path
from . import views


urlpatterns = [
	path('register/candidate/', views.register_candidate, name='register_candidate'),
	path('register/employer/', views.register_employer, name='register_employer'),
	path('login/', views.UserLoginView.as_view(), name='login'),
	path('logout/', views.UserLogoutView.as_view(), name='logout'),
]