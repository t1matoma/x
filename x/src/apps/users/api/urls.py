from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login, name='auth-login'),
    path('auth/register/', views.register, name='auth-register'),
    path('auth/logout/', views.logout, name='auth-logout'),
    path('auth/refresh/', views.refresh_token, name='auth-refresh'),

    # User management endpoints
    path('', views.user_list, name='user-list'),
    path('create/', views.create_user, name='user-create'),
    path('me/', views.current_user, name='current-user'),
    path('change-password/', views.change_password, name='change-password'),
    path('search/', views.search_users, name='search-users'),
    path('<int:user_id>/', views.user_detail, name='user-detail'),
    path('<int:user_id>/update/', views.update_user, name='user-update'),
    path('<int:user_id>/delete/', views.delete_user, name='user-delete'),
]

