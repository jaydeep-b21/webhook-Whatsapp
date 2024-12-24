from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('admin_interface/', views.admin_interface, name='admin_interface'),
    path('reply_to_user/', views.reply_to_user, name='reply_to_user'),
]