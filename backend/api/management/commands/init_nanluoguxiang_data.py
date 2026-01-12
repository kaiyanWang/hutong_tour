"""
Django management command to initialize Nanluoguxiang Hutong data.
Creates the hutong, POIs, and recommended routes with real location data.
"""
from django.core.management.base import BaseCommand
from api.models import Hutong, POI, Route, RoutePOI


class Command(BaseCommand):
    help = 'Initialize Nanluoguxiang Hutong data with POIs and routes'

    def handle(self, *args, **options):
        self.stdout.write('Initializing Nanluoguxiang data...')
        
        # Clear existing data
        RoutePOI.objects.all().delete()
        Route.objects.all().delete()
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # Create Nanluoguxiang Hutong
        hutong = Hutong.objects.create(
            name='南锣鼓巷',
            introduction='南锣鼓巷是北京最古老的街区之一，位于北京市东城区，是北京最具特色的胡同之一。这条胡同全长787米，宽8米，与元大都同期建成，至今已有740多年的历史。南锣鼓巷及周边区域曾是元大都的市中心，明清时期则是达官显贵的居住地。如今，这里已成为北京最热门的旅游景点之一，汇集了众多特色店铺、咖啡馆、酒吧和文创小店。',
            history='南锣鼓巷始建于元代，是元大都的重要组成部分。明清时期，这里是北京城内最繁华的地区之一，许多王公贵族在此建造府邸。清朝末年至民国时期，南锣鼓巷逐渐成为普通市民的居住区。2006年，南锣鼓巷被列为北京市历史文化保护街区，经过修缮改造后成为著名的文化旅游街区。这里保存了大量明清时期的四合院建筑，是了解老北京胡同文化的绝佳去处。',
            image='https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800',
            latitude=39.937,
            longitude=116.403
        )
        self.stdout.write(self.style.SUCCESS(f'Created hutong: {hutong.name}'))
        
        # Create POIs (at least 8 with real information)
        pois_data = [
            {
                'name': '僧格林沁王府',
                'category': 'historic',
                'description': '僧格林沁王府位于南锣鼓巷南口，是清代蒙古亲王僧格林沁的府邸。僧格林沁是清朝著名将领，曾在第二次鸦片战争中抵抗英法联军。王府建于清道光年间，占地面积约一万平方米，是典型的清代王府建筑。虽然现在大部分建筑已改作他用，但仍保留了部分原有格局，是研究清代王府建筑的重要实例。',
                'brief': '清代蒙古亲王僧格林沁的府邸，典型的清代王府建筑',
                'images': ['https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800'],
                'latitude': 39.9345,
                'longitude': 116.4028,
                'address': '北京市东城区南锣鼓巷南口'
            },
            {
                'name': '齐白石旧居纪念馆',
                'category': 'culture',
                'description': '齐白石旧居纪念馆位于雨儿胡同13号，是中国近现代著名画家齐白石晚年居住和创作的地方。齐白石（1864-1957）是中国20世纪最伟大的艺术家之一，以画虾、蟹、花鸟著称。这座四合院是典型的北京传统民居，齐白石在此度过了人生最后的岁月，创作了大量传世佳作。纪念馆内展示了齐白石的生平事迹和部分作品复制品。',
                'brief': '著名画家齐白石晚年居住创作之地，展示其生平与艺术成就',
                'images': ['https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=800'],
                'latitude': 39.9378,
                'longitude': 116.4035,
                'address': '北京市东城区雨儿胡同13号'
            },
            {
                'name': '茅盾故居',
                'category': 'culture',
                'description': '茅盾故居位于后圆恩寺胡同13号，是中国现代著名作家茅盾（沈雁冰）1974年至1981年居住的地方。茅盾是中国现代文学的奠基人之一，代表作有《子夜》《林家铺子》等。故居是一座典型的北京四合院，保存完好，现已辟为纪念馆，展示茅盾的生平、著作和遗物。院内环境幽静，是了解中国现代文学史的重要场所。',
                'brief': '中国现代著名作家茅盾晚年居所，现为纪念馆',
                'images': ['https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=800'],
                'latitude': 39.9385,
                'longitude': 116.4042,
                'address': '北京市东城区后圆恩寺胡同13号'
            },
            {
                'name': '文宇奶酪店',
                'category': 'food',
                'description': '文宇奶酪店是南锣鼓巷最著名的小吃店之一，以传统北京宫廷奶酪闻名。这家店创立于1990年代，坚持使用传统工艺制作奶酪，口感细腻醇厚，深受游客喜爱。除了招牌奶酪，店内还供应双皮奶、酸梅汤等传统甜品。每到旅游旺季，店门口常常排起长队，是来南锣鼓巷必打卡的美食店。',
                'brief': '南锣鼓巷最著名的传统北京宫廷奶酪店',
                'images': ['https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800'],
                'latitude': 39.9365,
                'longitude': 116.4032,
                'address': '北京市东城区南锣鼓巷49号'
            },
            {
                'name': '创可贴8',
                'category': 'shop',
                'description': '创可贴8是南锣鼓巷最具代表性的文创店铺之一，以独特的北京文化创意产品著称。店内销售各种以老北京元素为主题的T恤、明信片、冰箱贴等文创产品，设计风格幽默诙谐，深受年轻人喜爱。店名"创可贴8"寓意用创意治愈生活，是南锣鼓巷文创产业的代表性店铺。',
                'brief': '以老北京元素为主题的特色文创店铺',
                'images': ['https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800'],
                'latitude': 39.9358,
                'longitude': 116.4030,
                'address': '北京市东城区南锣鼓巷61号'
            },
            {
                'name': '过客酒吧',
                'category': 'food',
                'description': '过客酒吧是南锣鼓巷最早的酒吧之一，创立于1999年，被誉为南锣鼓巷酒吧文化的开创者。酒吧装修风格独特，融合了老北京胡同文化与现代艺术元素。这里曾是许多文艺青年和背包客的聚集地，见证了南锣鼓巷从普通胡同到文化街区的转变。酒吧提供各种鸡尾酒和简餐，是体验南锣鼓巷夜生活的好去处。',
                'brief': '南锣鼓巷最早的酒吧，见证胡同文化变迁',
                'images': ['https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'],
                'latitude': 39.9372,
                'longitude': 116.4033,
                'address': '北京市东城区南锣鼓巷108号'
            },
            {
                'name': '中央戏剧学院',
                'category': 'culture',
                'description': '中央戏剧学院位于南锣鼓巷北口附近，是中国最高等的戏剧艺术学府。学院创建于1950年，培养了大批著名演员、导演和戏剧艺术家，如巩俐、章子怡、姜文等。校园内有多个剧场和排练厅，经常举办各类戏剧演出和艺术活动。虽然校园不对外开放，但其存在为南锣鼓巷增添了浓厚的艺术氛围。',
                'brief': '中国最高等戏剧学府，培养众多著名演员',
                'images': ['https://images.unsplash.com/photo-1503095396549-807759245b35?w=800'],
                'latitude': 39.9395,
                'longitude': 116.4038,
                'address': '北京市东城区东棉花胡同39号'
            },
            {
                'name': '蓑衣胡同',
                'category': 'scenic',
                'description': '蓑衣胡同是南锣鼓巷东侧的一条支巷，因形状像蓑衣而得名。这条胡同保存了大量原汁原味的老北京四合院，相比主街更加安静，是体验真正胡同生活的好地方。胡同内有多处历史建筑，包括一些名人故居。漫步其中，可以感受到老北京胡同的独特韵味，是摄影爱好者的热门取景地。',
                'brief': '保存完好的传统胡同，体验原汁原味老北京',
                'images': ['https://images.unsplash.com/photo-1470004914212-05527e49370b?w=800'],
                'latitude': 39.9368,
                'longitude': 116.4045,
                'address': '北京市东城区蓑衣胡同'
            },
            {
                'name': '黑芝麻胡同',
                'category': 'scenic',
                'description': '黑芝麻胡同位于南锣鼓巷西侧，是一条历史悠久的胡同。胡同内有多处清代四合院，建筑保存较为完整。这里曾是清代官员和富商的居住地，至今仍保留着浓厚的历史氛围。胡同内的13号院是一座典型的清代大宅院，曾是清末大学士文煜的宅邸，现为私人住宅。黑芝麻胡同是了解北京胡同历史的绝佳去处。',
                'brief': '历史悠久的胡同，保存多处清代四合院',
                'images': ['https://images.unsplash.com/photo-1464817739973-0128fe77aaa1?w=800'],
                'latitude': 39.9375,
                'longitude': 116.4018,
                'address': '北京市东城区黑芝麻胡同'
            },
            {
                'name': '吉祥小吃',
                'category': 'food',
                'description': '吉祥小吃是南锣鼓巷内一家经营传统北京小吃的店铺，提供各种地道的老北京美食。店内供应炸酱面、卤煮火烧、豆汁焦圈、炒肝等传统小吃，味道正宗，价格实惠。店面虽小，但常年客满，是品尝正宗北京小吃的好去处。店主坚持使用传统配方和工艺，力求还原老北京的味道。',
                'brief': '经营传统北京小吃的老字号，味道正宗',
                'images': ['https://images.unsplash.com/photo-1555126634-323283e090fa?w=800'],
                'latitude': 39.9362,
                'longitude': 116.4029,
                'address': '北京市东城区南锣鼓巷35号'
            }
        ]
        
        pois = []
        for poi_data in pois_data:
            poi = POI.objects.create(hutong=hutong, **poi_data)
            pois.append(poi)
            self.stdout.write(self.style.SUCCESS(f'Created POI: {poi.name}'))
        
        # Create Routes (at least 2)
        # Route 1: 文化探索路线
        route1 = Route.objects.create(
            name='文化名人探访路线',
            description='这条路线带您探访南锣鼓巷及周边胡同中的名人故居和文化场所。从齐白石旧居开始，途经茅盾故居，最后到达中央戏剧学院，全程约2小时。沿途可以了解中国近现代文化名人的生活轨迹，感受浓厚的文化艺术氛围。',
            duration=120,
            hutong=hutong
        )
        self.stdout.write(self.style.SUCCESS(f'Created route: {route1.name}'))
        
        # Route 1 POIs
        route1_pois = [
            (pois[1], 1),  # 齐白石旧居纪念馆
            (pois[2], 2),  # 茅盾故居
            (pois[6], 3),  # 中央戏剧学院
            (pois[0], 4),  # 僧格林沁王府
        ]
        for poi, order in route1_pois:
            RoutePOI.objects.create(route=route1, poi=poi, order=order)
        
        # Route 2: 美食购物路线
        route2 = Route.objects.create(
            name='美食文创体验路线',
            description='这条路线专为美食爱好者和购物达人设计。从南锣鼓巷南口出发，沿途品尝传统北京小吃，探访特色文创店铺，最后在过客酒吧小憩。全程约1.5小时，是体验南锣鼓巷现代文化氛围的最佳选择。',
            duration=90,
            hutong=hutong
        )
        self.stdout.write(self.style.SUCCESS(f'Created route: {route2.name}'))
        
        # Route 2 POIs
        route2_pois = [
            (pois[9], 1),  # 吉祥小吃
            (pois[3], 2),  # 文宇奶酪店
            (pois[4], 3),  # 创可贴8
            (pois[5], 4),  # 过客酒吧
        ]
        for poi, order in route2_pois:
            RoutePOI.objects.create(route=route2, poi=poi, order=order)
        
        # Route 3: 胡同漫步路线
        route3 = Route.objects.create(
            name='胡同深度漫步路线',
            description='这条路线带您深入南锣鼓巷周边的小胡同，体验原汁原味的老北京生活。从黑芝麻胡同开始，穿过蓑衣胡同，感受胡同的宁静与历史。全程约1小时，适合喜欢摄影和慢节奏旅行的游客。',
            duration=60,
            hutong=hutong
        )
        self.stdout.write(self.style.SUCCESS(f'Created route: {route3.name}'))
        
        # Route 3 POIs
        route3_pois = [
            (pois[8], 1),  # 黑芝麻胡同
            (pois[7], 2),  # 蓑衣胡同
            (pois[0], 3),  # 僧格林沁王府
        ]
        for poi, order in route3_pois:
            RoutePOI.objects.create(route=route3, poi=poi, order=order)
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized Nanluoguxiang data!'))
        self.stdout.write(f'Created: 1 Hutong, {len(pois)} POIs, 3 Routes')
