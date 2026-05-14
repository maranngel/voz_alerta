from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('trigger/', views.trigger_signal, name='trigger_signal'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
