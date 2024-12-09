from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Use custom logout view
    path('quiz/', views.quiz, name='quiz'),
    path('result/', views.result, name='result'),
    path('about/', views.about, name='about'),
]
