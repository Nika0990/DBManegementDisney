from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('add_movie', views.add_movie, name='add_movie'),
    path('query_results', views.query_results, name='query_results')
]