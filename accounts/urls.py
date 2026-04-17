from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Pages
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),

    # API (chamadas AJAX do frontend JS)
    path('api/login/',    views.api_login,    name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/logout/',   views.api_logout,   name='api_logout'),
    path('api/me/',       views.api_me,       name='api_me'),
]
