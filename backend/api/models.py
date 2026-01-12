from django.db import models
from django.contrib.auth.models import User


class Hutong(models.Model):
    """胡同模型"""
    name = models.CharField(max_length=100, verbose_name='名称')
    introduction = models.TextField(verbose_name='简介')
    history = models.TextField(verbose_name='历史')
    image = models.URLField(verbose_name='图片URL')
    latitude = models.FloatField(verbose_name='纬度')
    longitude = models.FloatField(verbose_name='经度')

    class Meta:
        verbose_name = '胡同'
        verbose_name_plural = '胡同'

    def __str__(self):
        return self.name


class POI(models.Model):
    """兴趣点/景点模型"""
    CATEGORY_CHOICES = [
        ('historic', '历史古迹'),
        ('shop', '特色店铺'),
        ('food', '美食餐饮'),
        ('culture', '文化场所'),
        ('scenic', '景观'),
    ]
    name = models.CharField(max_length=100, verbose_name='名称')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='分类')
    description = models.TextField(verbose_name='详细描述')
    brief = models.CharField(max_length=200, verbose_name='简介')
    images = models.JSONField(default=list, verbose_name='图片URL列表')
    latitude = models.FloatField(verbose_name='纬度')
    longitude = models.FloatField(verbose_name='经度')
    address = models.CharField(max_length=200, verbose_name='地址')
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='pois', verbose_name='所属胡同')

    class Meta:
        verbose_name = '景点'
        verbose_name_plural = '景点'

    def __str__(self):
        return self.name


class Route(models.Model):
    """推荐路线模型"""
    name = models.CharField(max_length=100, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    duration = models.IntegerField(verbose_name='预计时长(分钟)')
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='routes', verbose_name='所属胡同')

    class Meta:
        verbose_name = '路线'
        verbose_name_plural = '路线'

    def __str__(self):
        return self.name


class RoutePOI(models.Model):
    """路线-景点关联模型"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_pois', verbose_name='路线')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE, verbose_name='景点')
    order = models.IntegerField(verbose_name='顺序')

    class Meta:
        verbose_name = '路线景点'
        verbose_name_plural = '路线景点'
        ordering = ['order']

    def __str__(self):
        return f'{self.route.name} - {self.poi.name} ({self.order})'


class Favorite(models.Model):
    """用户收藏模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE, verbose_name='景点')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ['user', 'poi']

    def __str__(self):
        return f'{self.user.username} - {self.poi.name}'
