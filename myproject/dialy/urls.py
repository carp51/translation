from django.urls import path
from . import views


urlpatterns = [
    path('', views.translate, name='translate'),
    path('login/', views.login_view, name='registration/login'),
    path('logout/', views.logout_view, name='registration/logout'),
    path('signup/', views.signup_view, name='signup')
]