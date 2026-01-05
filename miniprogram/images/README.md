# TabBar 图标说明

请准备以下图标文件（建议尺寸 81x81 像素）：

1. `home.png` - 首页图标（未选中）
2. `home-active.png` - 首页图标（选中，红色）
3. `poi.png` - 景点图标（未选中）
4. `poi-active.png` - 景点图标（选中，红色）
5. `route.png` - 路线图标（未选中）
6. `route-active.png` - 路线图标（选中，红色）
7. `placeholder.png` - 图片占位符

## 推荐图标来源

- 阿里巴巴矢量图标库：https://www.iconfont.cn/
- 搜索关键词：首页、景点、路线、地图

## 临时解决方案

如果暂时没有图标，可以在 app.json 中删除 tabBar 的 iconPath 和 selectedIconPath 配置，
只保留 text 属性，小程序会显示纯文字标签。
