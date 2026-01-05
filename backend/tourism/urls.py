from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'hutong', views.HutongViewSet, basename='hutong')
router.register(r'pois', views.POIViewSet, basename='poi')
router.register(r'routes', views.RouteViewSet, basename='route')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.search_pois, name='search'),
]
