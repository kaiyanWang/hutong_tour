from django.contrib import admin
from .models import Hutong, POICategory, POI, Route, RoutePoint, Favorite


@admin.register(Hutong)
class HutongAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['name']


@admin.register(POICategory)
class POICategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


class RoutePointInline(admin.TabularInline):
    model = RoutePoint
    extra = 1


@admin.register(POI)
class POIAdmin(admin.ModelAdmin):
    list_display = ['name', 'hutong', 'category', 'address', 'order']
    list_filter = ['hutong', 'category']
    search_fields = ['name', 'description']
    list_editable = ['order']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'hutong', 'duration', 'difficulty']
    list_filter = ['hutong', 'difficulty']
    inlines = [RoutePointInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['poi', 'session_key', 'created_at']
