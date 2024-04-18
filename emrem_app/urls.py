from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_reminder, name='create_reminder'),
    path('view/', views.view_reminders, name='view_reminders'),
    path('login/', auth_views.LoginView.as_view(template_name='emrem_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('reminder/<int:pk>/', views.ReminderDetailView.as_view(), name='reminder-title'),
    path('edit-reminder/<int:pk>/', views.edit_reminder, name='edit_reminder'),
    path('delete-reminder/<int:pk>/', views.delete_reminder, name='delete_reminder'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
]