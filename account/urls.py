from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('edit', views.editProfile, name='edit_profile'),
    path('delete', views.deleteProfile, name='delete_profile'),
    path('logout', views.logout, name='logout'),
]

