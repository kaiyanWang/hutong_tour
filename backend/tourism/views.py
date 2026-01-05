from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Hutong, POI, Route
from .serializers import (
    HutongSerializer, POIListSerializer, POIDetailSerializer,
    RouteListSerializer, RouteDetailSerializer
)


class HutongViewSet(viewsets.ReadOnlyModelViewSet):
    """胡同信息视图集"""
    queryset = Hutong.objects.all()
    serializer_class = HutongSerializer
    pagination_class = None  # 胡同信息不需要分页

    def list(self, request):
        """获取胡同信息（返回第一条）"""
        hutong = self.queryset.first()
        if hutong:
            serializer = self.get_serializer(hutong)
            return Response(serializer.data)
        return Response({"detail": "暂无胡同信息"}, status=status.HTTP_404_NOT_FOUND)


class POIViewSet(viewsets.ReadOnlyModelViewSet):
    """POI视图集"""
    queryset = POI.objects.all().order_by('order', 'id')

    def get_serializer_class(self):
        if self.action == 'list':
            return POIListSerializer
        return POIDetailSerializer

    def list(self, request):
        """获取POI列表"""
        queryset = self.get_queryset()
        serializer = POIListSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    """推荐路线视图集"""
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteListSerializer
        return RouteDetailSerializer

    def list(self, request):
        """获取路线列表"""
        queryset = self.get_queryset()
        serializer = RouteListSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })


@api_view(['GET'])
def search_pois(request):
    """搜索POI"""
    keyword = request.query_params.get('q', '').strip()
    if not keyword:
        return Response({
            'count': 0,
            'results': [],
            'message': '请输入搜索关键词'
        })

    pois = POI.objects.filter(
        Q(name__icontains=keyword) | Q(description__icontains=keyword)
    ).order_by('order', 'id')

    serializer = POIListSerializer(pois, many=True)
    return Response({
        'count': pois.count(),
        'results': serializer.data
    })
