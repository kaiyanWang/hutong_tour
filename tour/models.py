from django.db import models


class Hutong(models.Model):
    """胡同基本信息"""
    name = models.CharField('胡同名称', max_length=100)
    description = models.TextField('胡同简介')
    history = models.TextField('历史背景', blank=True)
    location = models.CharField('地理位置', max_length=200)
    image = models.ImageField('封面图片', upload_to='hutong/', blank=True)
    
    class Meta:
        verbose_name = '胡同'
        verbose_name_plural = '胡同'
    
    def __str__(self):
        return self.name


class POICategory(models.Model):
    """POI分类"""
    name = models.CharField('分类名称', max_length=50)
    icon = models.CharField('图标', max_length=50, default='fa-map-marker')
    
    class Meta:
        verbose_name = 'POI分类'
        verbose_name_plural = 'POI分类'
    
    def __str__(self):
        return self.name


class POI(models.Model):
    """兴趣点"""
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='pois', verbose_name='所属胡同')
    category = models.ForeignKey(POICategory, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    name = models.CharField('名称', max_length=100)
    description = models.TextField('简介')
    detail = models.TextField('详细介绍', blank=True)
    address = models.CharField('地址', max_length=200)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, null=True, blank=True)
    image = models.ImageField('图片', upload_to='poi/', blank=True)
    opening_hours = models.CharField('开放时间', max_length=100, blank=True)
    ticket_price = models.CharField('门票价格', max_length=100, blank=True)
    order = models.IntegerField('排序', default=0)
    
    class Meta:
        verbose_name = 'POI景点'
        verbose_name_plural = 'POI景点'
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.name


class Route(models.Model):
    """推荐路线"""
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='routes', verbose_name='所属胡同')
    name = models.CharField('路线名称', max_length=100)
    description = models.TextField('路线简介')
    duration = models.CharField('预计时长', max_length=50)
    distance = models.CharField('路线长度', max_length=50, blank=True)
    difficulty = models.CharField('难度', max_length=20, default='简单')
    
    class Meta:
        verbose_name = '推荐路线'
        verbose_name_plural = '推荐路线'
    
    def __str__(self):
        return self.name


class RoutePoint(models.Model):
    """路线点"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points', verbose_name='所属路线')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE, verbose_name='关联POI')
    order = models.IntegerField('顺序')
    tips = models.TextField('游览提示', blank=True)
    
    class Meta:
        verbose_name = '路线点'
        verbose_name_plural = '路线点'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.route.name} - {self.order}. {self.poi.name}"


class Favorite(models.Model):
    """收藏"""
    poi = models.ForeignKey(POI, on_delete=models.CASCADE, verbose_name='收藏的POI')
    session_key = models.CharField('会话标识', max_length=100)
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ['poi', 'session_key']
