from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_reminder, name='create_reminder'),
    path('view/', views.view_reminders, name='view_reminders'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reminder/<int:pk>/', views.ReminderDetailView.as_view(), name='reminder-title'),
    path('edit-reminder/<int:pk>/', views.edit_reminder, name='edit_reminder'),
    path('delete-reminder/<int:pk>/', views.delete_reminder, name='delete_reminder'),
]