from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flood-form/', views.location_submit_view, name='flood_form'),
]

