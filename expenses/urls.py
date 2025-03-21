from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('expenses', views.add_expences, name="expenses"),
]