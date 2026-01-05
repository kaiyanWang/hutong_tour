from rest_framework import serializers
from .models import Hutong, POI, Route, RoutePOI


class HutongSerializer(serializers.ModelSerializer):
    """胡同信息序列化器"""
    class Meta:
        model = Hutong
        fields = ['id', 'name', 'description', 'location', 'history', 'features', 'image', 'created_at']


class POIListSerializer(serializers.ModelSerializer):
    """POI列表序列化器"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = POI
        fields = ['id', 'name', 'type', 'type_display', 'brief', 'thumbnail', 'location']

    def get_thumbnail(self, obj):
        if obj.images and len(obj.images) > 0:
            return obj.images[0]
        return None


class POIDetailSerializer(serializers.ModelSerializer):
    """POI详情序列化器"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = POI
        fields = [
            'id', 'name', 'type', 'type_display', 'description', 'brief',
            'location', 'coordinates', 'images', 'opening_hours', 'tips', 'created_at'
        ]


class RoutePOISerializer(serializers.ModelSerializer):
    """路线POI关联序列化器"""
    poi = POIListSerializer(read_only=True)

    class Meta:
        model = RoutePOI
        fields = ['order', 'poi']


class RouteListSerializer(serializers.ModelSerializer):
    """路线列表序列化器"""
    poi_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'name', 'description', 'duration', 'distance', 'poi_count']

    def get_poi_count(self, obj):
        return obj.route_pois.count()


class RouteDetailSerializer(serializers.ModelSerializer):
    """路线详情序列化器"""
    pois = RoutePOISerializer(source='route_pois', many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'description', 'duration', 'distance', 'pois', 'created_at']
