from django.contrib import admin
from .models import Hutong, POI, Route, RoutePOI, Favorite


@admin.register(Hutong)
class HutongAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'latitude', 'longitude']
    search_fields = ['name']


@admin.register(POI)
class POIAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'address', 'hutong']
    list_filter = ['category', 'hutong']
    search_fields = ['name', 'address']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'duration', 'hutong']
    list_filter = ['hutong']
    search_fields = ['name']


@admin.register(RoutePOI)
class RoutePOIAdmin(admin.ModelAdmin):
    list_display = ['id', 'route', 'poi', 'order']
    list_filter = ['route']
    ordering = ['route', 'order']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'poi', 'created_at']
    list_filter = ['user', 'poi']
    search_fields = ['user__username', 'poi__name']
