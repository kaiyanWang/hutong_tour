from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Hutong, POI, Route, RoutePOI, Favorite


class HutongSerializer(serializers.ModelSerializer):
    """胡同序列化器"""
    class Meta:
        model = Hutong
        fields = ['id', 'name', 'introduction', 'history', 'image', 'latitude', 'longitude']


class POIListSerializer(serializers.ModelSerializer):
    """POI列表序列化器"""
    class Meta:
        model = POI
        fields = ['id', 'name', 'category', 'brief', 'images', 'latitude', 'longitude']


class POIDetailSerializer(serializers.ModelSerializer):
    """POI详情序列化器"""
    class Meta:
        model = POI
        fields = ['id', 'name', 'category', 'description', 'brief', 'images', 'latitude', 'longitude', 'address', 'hutong']


class RegisterSerializer(serializers.Serializer):
    """用户注册序列化器"""
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate(self, data):
        """验证密码匹配"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "两次输入的密码不一致"})
        return data

    def create(self, validated_data):
        """创建用户"""
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RoutePOISerializer(serializers.ModelSerializer):
    """路线景点序列化器（用于路线详情中的POI列表）"""
    id = serializers.IntegerField(source='poi.id')
    name = serializers.CharField(source='poi.name')
    category = serializers.CharField(source='poi.category')
    brief = serializers.CharField(source='poi.brief')
    latitude = serializers.FloatField(source='poi.latitude')
    longitude = serializers.FloatField(source='poi.longitude')
    address = serializers.CharField(source='poi.address')

    class Meta:
        model = RoutePOI
        fields = ['id', 'name', 'category', 'brief', 'latitude', 'longitude', 'address', 'order']


class RouteListSerializer(serializers.ModelSerializer):
    """路线列表序列化器"""
    poi_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'name', 'duration', 'poi_count']

    def get_poi_count(self, obj):
        return obj.route_pois.count()


class RouteDetailSerializer(serializers.ModelSerializer):
    """路线详情序列化器"""
    poi_count = serializers.SerializerMethodField()
    pois = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'name', 'description', 'duration', 'poi_count', 'pois']

    def get_poi_count(self, obj):
        return obj.route_pois.count()

    def get_pois(self, obj):
        route_pois = obj.route_pois.all().order_by('order')
        return RoutePOISerializer(route_pois, many=True).data


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    poi = POIListSerializer(read_only=True)
    poi_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'poi', 'poi_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """创建收藏"""
        user = self.context['request'].user
        poi_id = validated_data['poi_id']
        poi = POI.objects.get(pk=poi_id)
        favorite, created = Favorite.objects.get_or_create(user=user, poi=poi)
        return favorite
