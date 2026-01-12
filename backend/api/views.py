from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import (
    RegisterSerializer, LoginSerializer, HutongSerializer, 
    POIListSerializer, POIDetailSerializer,
    RouteListSerializer, RouteDetailSerializer,
    FavoriteSerializer
)
from .models import Hutong, POI, Route, Favorite


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册API"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': '注册成功',
            'user_id': user.id,
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录API"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': '登录成功',
                'user_id': user.id,
                'username': user.username,
                'token': token.key
            })
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """用户登出API"""
    try:
        request.user.auth_token.delete()
        return Response({'message': '登出成功'})
    except Exception:
        return Response({'error': '登出失败'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def hutong_overview(request):
    """获取胡同概览API"""
    hutong = Hutong.objects.first()
    if hutong:
        serializer = HutongSerializer(hutong)
        return Response(serializer.data)
    return Response({'error': '胡同数据不存在'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def poi_list(request):
    """获取POI列表API"""
    pois = POI.objects.all()
    serializer = POIListSerializer(pois, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def poi_detail(request, pk):
    """获取POI详情API"""
    try:
        poi = POI.objects.get(pk=pk)
        serializer = POIDetailSerializer(poi)
        return Response(serializer.data)
    except POI.DoesNotExist:
        return Response({'error': '景点不存在'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def poi_search(request):
    """搜索POI API"""
    keyword = request.query_params.get('q', '')
    if keyword:
        pois = POI.objects.filter(name__icontains=keyword)
    else:
        pois = POI.objects.none()
    serializer = POIListSerializer(pois, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def route_list(request):
    """获取路线列表API"""
    routes = Route.objects.all()
    serializer = RouteListSerializer(routes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def route_detail(request, pk):
    """获取路线详情API"""
    try:
        route = Route.objects.get(pk=pk)
        serializer = RouteDetailSerializer(route)
        return Response(serializer.data)
    except Route.DoesNotExist:
        return Response({'error': '路线不存在'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    """获取用户收藏列表API"""
    favorites = Favorite.objects.filter(user=request.user).select_related('poi')
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_add(request):
    """添加收藏API"""
    poi_id = request.data.get('poi_id')
    if not poi_id:
        return Response({'error': '缺少poi_id参数'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        poi = POI.objects.get(pk=poi_id)
    except POI.DoesNotExist:
        return Response({'error': '景点不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, poi=poi)
    if created:
        return Response({'message': '收藏成功', 'id': favorite.id}, status=status.HTTP_201_CREATED)
    return Response({'message': '已经收藏过了', 'id': favorite.id}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def favorite_delete(request, poi_id):
    """删除收藏API"""
    try:
        favorite = Favorite.objects.get(user=request.user, poi_id=poi_id)
        favorite.delete()
        return Response({'message': '取消收藏成功'})
    except Favorite.DoesNotExist:
        return Response({'error': '收藏不存在'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def poi_is_favorite(request, pk):
    """检查POI是否已收藏API"""
    is_favorite = Favorite.objects.filter(user=request.user, poi_id=pk).exists()
    return Response({'is_favorite': is_favorite})
