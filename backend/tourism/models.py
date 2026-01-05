from django.db import models


class Hutong(models.Model):
    """胡同信息模型"""
    name = models.CharField(max_length=100, verbose_name="胡同名称")
    description = models.TextField(verbose_name="详细介绍")
    location = models.CharField(max_length=200, verbose_name="地理位置")
    history = models.TextField(verbose_name="历史沿革")
    features = models.JSONField(default=list, verbose_name="特色标签")
    image = models.CharField(max_length=500, verbose_name="封面图片")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "胡同"
        verbose_name_plural = "胡同"

    def __str__(self):
        return self.name


class POI(models.Model):
    """兴趣点模型"""
    TYPE_CHOICES = [
        ('historic', '历史古迹'),
        ('celebrity', '名人故居'),
        ('shop', '特色店铺'),
        ('food', '美食餐饮'),
        ('culture', '文化场所'),
        ('other', '其他'),
    ]

    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='pois')
    name = models.CharField(max_length=100, verbose_name="名称")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="类型")
    description = models.TextField(verbose_name="详细介绍")
    brief = models.CharField(max_length=200, verbose_name="简短描述")
    location = models.CharField(max_length=200, verbose_name="具体位置")
    coordinates = models.JSONField(null=True, blank=True, verbose_name="坐标")
    images = models.JSONField(default=list, verbose_name="图片列表")
    opening_hours = models.CharField(max_length=100, blank=True, verbose_name="开放时间")
    tips = models.CharField(max_length=200, blank=True, verbose_name="游览提示")
    order = models.IntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "兴趣点"
        verbose_name_plural = "兴趣点"
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class Route(models.Model):
    """推荐路线模型"""
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=100, verbose_name="路线名称")
    description = models.TextField(verbose_name="路线介绍")
    duration = models.CharField(max_length=50, verbose_name="预计时间")
    distance = models.CharField(max_length=50, verbose_name="路线长度")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "推荐路线"
        verbose_name_plural = "推荐路线"

    def __str__(self):
        return self.name


class RoutePOI(models.Model):
    """路线-POI关联模型"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_pois')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name="顺序")

    class Meta:
        verbose_name = "路线景点"
        verbose_name_plural = "路线景点"
        ordering = ['order']
        unique_together = ['route', 'poi']

    def __str__(self):
        return f"{self.route.name} - {self.poi.name}"
