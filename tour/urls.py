from django.urls import path
from . import views

app_name = 'tour'

urlpatterns = [
    path('', views.index, name='index'),
    path('pois/', views.poi_list, name='poi_list'),
    path('poi/<int:pk>/', views.poi_detail, name='poi_detail'),
    path('routes/', views.route_list, name='route_list'),
    path('route/<int:pk>/', views.route_detail, name='route_detail'),
    path('search/', views.search, name='search'),
    path('favorites/', views.favorites, name='favorites'),
    path('api/favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
]
