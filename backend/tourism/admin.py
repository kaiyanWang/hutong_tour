from django.contrib import admin
from .models import Hutong, POI, Route, RoutePOI


@admin.register(Hutong)
class HutongAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'created_at']
    search_fields = ['name', 'description']


@admin.register(POI)
class POIAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'location', 'order', 'created_at']
    list_filter = ['type', 'hutong']
    search_fields = ['name', 'description']
    ordering = ['order', 'id']


class RoutePOIInline(admin.TabularInline):
    model = RoutePOI
    extra = 1


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'distance', 'created_at']
    search_fields = ['name', 'description']
    inlines = [RoutePOIInline]
