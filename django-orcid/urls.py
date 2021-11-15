### URLS will go here###
from django.urls import path
from orcidaccount import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'auth', views.auth, name='auth'),
    path(r'profile', views.profile, name='profile'),
    path(r'login',views.login,name='login'),
    path(r'login/', views.login),
    path(r'logout', auth_views.LogoutView.as_view(template_name='./logout.html'), name='logout'),
    path(r'logout/',auth_views.LogoutView.as_view(template_name='./logout.html')),
    path(r'delete',views.delete_account, name='delete_account'),
    path(r'delete/',views.delete_account),
]