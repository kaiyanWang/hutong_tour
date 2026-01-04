from django.core.management.base import BaseCommand
from tour.models import Hutong, POICategory, POI, Route, RoutePoint


class Command(BaseCommand):
    help = '初始化南锣鼓巷示例数据'

    def handle(self, *args, **options):
        # 创建胡同
        hutong, _ = Hutong.objects.get_or_create(
            name='南锣鼓巷',
            defaults={
                'description': '南锣鼓巷是北京最古老的街区之一，位于北京中轴线东侧的交道口地区，北起鼓楼东大街，南至平安大街，全长787米，宽8米。这里保存着规模最大、品级最高、资源最丰富的棋盘式传统民居区。',
                'history': '南锣鼓巷始建于元大都时期，至今已有740多年历史。明清时期，这里是达官贵人的居住地，留下了众多名人故居和历史遗迹。如今，南锣鼓巷已成为北京最具特色的文化创意街区之一。',
                'location': '北京市东城区南锣鼓巷',
            }
        )

        # 创建分类
        categories = {
            '历史古迹': POICategory.objects.get_or_create(name='历史古迹', defaults={'icon': 'fa-landmark'})[0],
            '名人故居': POICategory.objects.get_or_create(name='名人故居', defaults={'icon': 'fa-home'})[0],
            '特色店铺': POICategory.objects.get_or_create(name='特色店铺', defaults={'icon': 'fa-store'})[0],
            '美食餐饮': POICategory.objects.get_or_create(name='美食餐饮', defaults={'icon': 'fa-utensils'})[0],
            '文化场所': POICategory.objects.get_or_create(name='文化场所', defaults={'icon': 'fa-theater-masks'})[0],
        }

        # 创建POI数据
        pois_data = [
            {
                'name': '齐白石旧居纪念馆',
                'category': '名人故居',
                'description': '国画大师齐白石晚年居住和创作的地方',
                'detail': '齐白石旧居位于南锣鼓巷雨儿胡同13号，是一座典型的北京四合院。齐白石先生于1955年至1957年在此居住，创作了大量传世名作。馆内陈列着齐白石的生平介绍、书画作品复制品及生活用品等。',
                'address': '东城区雨儿胡同13号',
                'opening_hours': '9:00-17:00（周一闭馆）',
                'ticket_price': '免费',
                'order': 1,
            },
            {
                'name': '茅盾故居',
                'category': '名人故居',
                'description': '著名作家茅盾先生的故居',
                'detail': '茅盾故居位于后圆恩寺胡同13号，是茅盾先生1974年至1981年居住的地方。故居为两进四合院，保存完好，现已辟为茅盾纪念馆，展示茅盾先生的生平事迹和文学成就。',
                'address': '东城区后圆恩寺胡同13号',
                'opening_hours': '9:00-16:00（周一闭馆）',
                'ticket_price': '免费',
                'order': 2,
            },
            {
                'name': '僧格林沁王府',
                'category': '历史古迹',
                'description': '清代蒙古亲王僧格林沁的府邸',
                'detail': '僧格林沁王府位于炒豆胡同，是清代著名将领僧格林沁的府邸。僧格林沁是清朝末年抗击太平天国和英法联军的名将。王府建筑宏伟，虽经历史变迁，仍保留着部分原有格局。',
                'address': '东城区炒豆胡同73号',
                'opening_hours': '外观可参观',
                'ticket_price': '免费',
                'order': 3,
            },
            {
                'name': '蓑衣胡同',
                'category': '历史古迹',
                'description': '保存完好的明清胡同',
                'detail': '蓑衣胡同是南锣鼓巷地区保存最完好的胡同之一，胡同内有多处明清时期的四合院建筑。漫步其中，可以感受到老北京胡同的原汁原味。',
                'address': '东城区蓑衣胡同',
                'opening_hours': '全天开放',
                'ticket_price': '免费',
                'order': 4,
            },
            {
                'name': '文宇奶酪店',
                'category': '美食餐饮',
                'description': '南锣鼓巷最有名的老北京奶酪店',
                'detail': '文宇奶酪店是南锣鼓巷最具人气的小吃店之一，主打老北京传统奶酪。店铺虽小，但奶酪口感醇厚，深受游客喜爱。招牌产品有原味奶酪、双皮奶等。',
                'address': '南锣鼓巷49号',
                'opening_hours': '10:00-22:00',
                'ticket_price': '人均20-30元',
                'order': 5,
            },
            {
                'name': '过客酒吧',
                'category': '特色店铺',
                'description': '南锣鼓巷最早的酒吧之一',
                'detail': '过客酒吧是南锣鼓巷最早开设的酒吧之一，也是北京文艺青年的聚集地。酒吧装修独特，氛围轻松，经常举办各类文化活动和音乐演出。',
                'address': '南锣鼓巷108号',
                'opening_hours': '14:00-02:00',
                'ticket_price': '人均50-100元',
                'order': 6,
            },
            {
                'name': '创可贴8',
                'category': '特色店铺',
                'description': '创意文化产品店',
                'detail': '创可贴8是一家以北京文化为主题的创意产品店，店内售卖各种具有北京特色的文创产品，如胡同主题T恤、明信片、冰箱贴等，是购买伴手礼的好去处。',
                'address': '南锣鼓巷61号',
                'opening_hours': '10:00-22:00',
                'ticket_price': '免费参观',
                'order': 7,
            },
            {
                'name': '中央戏剧学院',
                'category': '文化场所',
                'description': '中国顶尖的戏剧艺术学府',
                'detail': '中央戏剧学院位于南锣鼓巷附近的东棉花胡同，是中国戏剧艺术教育的最高学府。校园内有实验剧场，经常上演学生和教师的戏剧作品，是戏剧爱好者的朝圣之地。',
                'address': '东城区东棉花胡同39号',
                'opening_hours': '校园开放时间不定',
                'ticket_price': '演出票价不等',
                'order': 8,
            },
            {
                'name': '黑芝麻胡同',
                'category': '历史古迹',
                'description': '充满历史韵味的老胡同',
                'detail': '黑芝麻胡同是南锣鼓巷东侧的一条胡同，胡同内保存着多处历史建筑。这里曾是清代官员的居住地，如今仍保留着浓厚的老北京生活气息。',
                'address': '东城区黑芝麻胡同',
                'opening_hours': '全天开放',
                'ticket_price': '免费',
                'order': 9,
            },
            {
                'name': '鬼味烤翅',
                'category': '美食餐饮',
                'description': '南锣鼓巷人气烤翅店',
                'detail': '鬼味烤翅是南锣鼓巷的网红美食店，以独特的烤翅口味闻名。烤翅外焦里嫩，配上秘制酱料，深受年轻人喜爱。',
                'address': '南锣鼓巷85号',
                'opening_hours': '11:00-23:00',
                'ticket_price': '人均30-50元',
                'order': 10,
            },
        ]

        for poi_data in pois_data:
            category = categories.get(poi_data.pop('category'))
            POI.objects.get_or_create(
                hutong=hutong,
                name=poi_data['name'],
                defaults={**poi_data, 'category': category}
            )

        # 创建推荐路线
        route1, _ = Route.objects.get_or_create(
            hutong=hutong,
            name='经典文化游',
            defaults={
                'description': '探访南锣鼓巷的名人故居和历史古迹，感受老北京的文化底蕴。',
                'duration': '2-3小时',
                'distance': '约2公里',
                'difficulty': '简单',
            }
        )

        route2, _ = Route.objects.get_or_create(
            hutong=hutong,
            name='美食探店游',
            defaults={
                'description': '品尝南锣鼓巷的特色美食，体验地道的北京小吃文化。',
                'duration': '1.5-2小时',
                'distance': '约1公里',
                'difficulty': '简单',
            }
        )

        # 创建路线点
        pois = {poi.name: poi for poi in POI.objects.filter(hutong=hutong)}
        
        route1_points = [
            ('齐白石旧居纪念馆', '建议参观30分钟，了解齐白石先生的艺术人生'),
            ('茅盾故居', '建议参观20分钟，感受文学大师的生活环境'),
            ('僧格林沁王府', '外观参观，了解清代王府建筑'),
            ('黑芝麻胡同', '漫步胡同，感受老北京生活'),
            ('中央戏剧学院', '如有演出可观看'),
        ]

        for i, (name, tips) in enumerate(route1_points, 1):
            if name in pois:
                RoutePoint.objects.get_or_create(
                    route=route1,
                    poi=pois[name],
                    defaults={'order': i, 'tips': tips}
                )

        route2_points = [
            ('文宇奶酪店', '必尝招牌原味奶酪'),
            ('鬼味烤翅', '人气烤翅，建议下午去避开排队'),
            ('创可贴8', '购买北京特色文创伴手礼'),
            ('过客酒吧', '傍晚可以在这里小憩'),
        ]

        for i, (name, tips) in enumerate(route2_points, 1):
            if name in pois:
                RoutePoint.objects.get_or_create(
                    route=route2,
                    poi=pois[name],
                    defaults={'order': i, 'tips': tips}
                )

        self.stdout.write(self.style.SUCCESS('成功初始化南锣鼓巷数据！'))
