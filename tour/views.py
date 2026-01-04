from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Hutong, POI, POICategory, Route, Favorite


def index(request):
    """首页 - 胡同概览"""
    hutong = Hutong.objects.first()
    pois = POI.objects.filter(hutong=hutong)[:6] if hutong else []
    routes = Route.objects.filter(hutong=hutong)[:2] if hutong else []
    return render(request, 'tour/index.html', {
        'hutong': hutong,
        'pois': pois,
        'routes': routes,
    })


def poi_list(request):
    """POI列表"""
    hutong = Hutong.objects.first()
    categories = POICategory.objects.all()
    category_id = request.GET.get('category')
    search = request.GET.get('search', '').strip()
    
    pois = POI.objects.filter(hutong=hutong) if hutong else POI.objects.none()
    
    if category_id:
        pois = pois.filter(category_id=category_id)
    if search:
        pois = pois.filter(name__icontains=search) | pois.filter(description__icontains=search)
    
    return render(request, 'tour/poi_list.html', {
        'hutong': hutong,
        'pois': pois,
        'categories': categories,
        'current_category': category_id,
        'search': search,
    })


def poi_detail(request, pk):
    """POI详情"""
    poi = get_object_or_404(POI, pk=pk)
    session_key = request.session.session_key or ''
    is_favorited = Favorite.objects.filter(poi=poi, session_key=session_key).exists() if session_key else False
    
    # 获取相关POI
    related_pois = POI.objects.filter(hutong=poi.hutong).exclude(pk=pk)[:4]
    
    return render(request, 'tour/poi_detail.html', {
        'poi': poi,
        'is_favorited': is_favorited,
        'related_pois': related_pois,
    })


def route_list(request):
    """路线列表"""
    hutong = Hutong.objects.first()
    routes = Route.objects.filter(hutong=hutong) if hutong else []
    return render(request, 'tour/route_list.html', {
        'hutong': hutong,
        'routes': routes,
    })


def route_detail(request, pk):
    """路线详情"""
    route = get_object_or_404(Route, pk=pk)
    points = route.points.select_related('poi').all()
    return render(request, 'tour/route_detail.html', {
        'route': route,
        'points': points,
    })


def search(request):
    """搜索"""
    query = request.GET.get('q', '').strip()
    pois = []
    if query:
        pois = POI.objects.filter(name__icontains=query) | POI.objects.filter(description__icontains=query)
    return render(request, 'tour/search.html', {
        'query': query,
        'pois': pois,
    })


def favorites(request):
    """收藏列表"""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    favorite_pois = POI.objects.filter(favorite__session_key=session_key)
    return render(request, 'tour/favorites.html', {
        'pois': favorite_pois,
    })


@require_POST
def toggle_favorite(request, pk):
    """切换收藏状态"""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    poi = get_object_or_404(POI, pk=pk)
    
    favorite, created = Favorite.objects.get_or_create(poi=poi, session_key=session_key)
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True
    
    return JsonResponse({'is_favorited': is_favorited})
