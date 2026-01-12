from django.urls import path
from . import views

urlpatterns = [
    # 用户认证API
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # 胡同API
    path('hutong/', views.hutong_overview, name='hutong_overview'),
    
    # POI API
    path('pois/', views.poi_list, name='poi_list'),
    path('pois/search/', views.poi_search, name='poi_search'),
    path('pois/<int:pk>/', views.poi_detail, name='poi_detail'),
    path('pois/<int:pk>/is_favorite/', views.poi_is_favorite, name='poi_is_favorite'),
    
    # 路线API
    path('routes/', views.route_list, name='route_list'),
    path('routes/<int:pk>/', views.route_detail, name='route_detail'),
    
    # 收藏API
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/add/', views.favorite_add, name='favorite_add'),
    path('favorites/<int:poi_id>/', views.favorite_delete, name='favorite_delete'),
]
