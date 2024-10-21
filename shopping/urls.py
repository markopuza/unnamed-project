from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.items_endpoint, name='items'),
    path('session-id/', views.get_session_id, name='get_session_id'),
]