"""
认证API属性测试
Feature: nanluoguxiang-tour
"""
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# 用户名策略：字母数字组合，长度3-10
username_strategy = st.text(
    alphabet='abcdefghijklmnopqrstuvwxyz',
    min_size=3,
    max_size=10
)

# 密码策略：8-15个字符
password_strategy = st.text(
    alphabet='abcdefghijklmnopqrstuvwxyz0123456789',
    min_size=8,
    max_size=15
)


@pytest.mark.django_db(transaction=True)
class TestAuthenticationProperties:
    """认证API属性测试类"""

    @settings(max_examples=30, deadline=None)
    @given(username=username_strategy, password=password_strategy)
    def test_property_1_registration_validation(self, username, password):
        """
        Property 1: Registration Validation
        *For any* registration request, the system should create a user account 
        if and only if the username is unique AND the password matches the confirm password.
        **Validates: Requirements 1.1, 1.2, 1.3**
        """
        client = APIClient()
        
        # 清理可能存在的用户
        User.objects.filter(username=username).delete()
        User.objects.filter(username=username + 'new').delete()
        
        # Case 1: 有效注册（用户名唯一，密码匹配）
        response = client.post('/api/register/', {
            'username': username,
            'password': password,
            'confirm_password': password
        })
        assert response.status_code == 201
        assert User.objects.filter(username=username).exists()
        
        # Case 2: 重复用户名应该被拒绝
        response2 = client.post('/api/register/', {
            'username': username,
            'password': password,
            'confirm_password': password
        })
        assert response2.status_code == 400
        
        # Case 3: 密码不匹配应该被拒绝
        new_username = username + 'new'
        response3 = client.post('/api/register/', {
            'username': new_username,
            'password': password,
            'confirm_password': password + 'x'
        })
        assert response3.status_code == 400
        assert not User.objects.filter(username=new_username).exists()
        
        # 清理
        User.objects.filter(username=username).delete()

    @settings(max_examples=30, deadline=None)
    @given(username=username_strategy, password=password_strategy)
    def test_property_2_login_authentication(self, username, password):
        """
        Property 2: Login Authentication
        *For any* login request with credentials (username, password), the system should 
        return a valid token if and only if the user exists AND the password is correct.
        **Validates: Requirements 1.4, 1.5**
        """
        client = APIClient()
        
        # 清理并创建测试用户
        User.objects.filter(username=username).delete()
        user = User.objects.create_user(username=username, password=password)
        
        # Case 1: 正确凭据应该返回token
        response = client.post('/api/login/', {
            'username': username,
            'password': password
        })
        assert response.status_code == 200
        assert 'token' in response.data
        
        # Case 2: 错误密码应该被拒绝
        response2 = client.post('/api/login/', {
            'username': username,
            'password': password + 'wrong'
        })
        assert response2.status_code == 401
        
        # Case 3: 不存在的用户应该被拒绝
        response3 = client.post('/api/login/', {
            'username': username + 'none',
            'password': password
        })
        assert response3.status_code == 401
        
        # 清理
        user.delete()

    @settings(max_examples=30, deadline=None)
    @given(username=username_strategy, password=password_strategy)
    def test_property_3_logout_invalidation(self, username, password):
        """
        Property 3: Logout Invalidation
        *For any* authenticated user session, after logout, the previously valid token 
        should no longer be accepted for authenticated requests.
        **Validates: Requirements 1.6**
        """
        client = APIClient()
        
        # 清理并创建测试用户
        User.objects.filter(username=username).delete()
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        
        # 使用token进行认证
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # 登出
        response = client.post('/api/logout/')
        assert response.status_code == 200
        
        # 登出后，使用相同token应该被拒绝
        response2 = client.post('/api/logout/')
        assert response2.status_code == 401
        
        # 清理
        User.objects.filter(username=username).delete()


from api.models import Hutong, POI


# POI名称策略
poi_name_strategy = st.text(
    alphabet='abcdefghijklmnopqrstuvwxyz中文测试',
    min_size=2,
    max_size=20
).filter(lambda x: len(x.strip()) >= 2)

# POI分类策略
poi_category_strategy = st.sampled_from(['historic', 'shop', 'food', 'culture', 'scenic'])

# 坐标策略
latitude_strategy = st.floats(min_value=39.0, max_value=41.0, allow_nan=False, allow_infinity=False)
longitude_strategy = st.floats(min_value=116.0, max_value=117.0, allow_nan=False, allow_infinity=False)


@pytest.mark.django_db(transaction=True)
class TestHutongAndPOIProperties:
    """胡同和POI API属性测试类"""

    def setup_method(self):
        """每个测试方法前清理数据"""
        POI.objects.all().delete()
        Hutong.objects.all().delete()

    @settings(max_examples=30, deadline=None)
    @given(
        name=st.text(alphabet='abcdefghijklmnopqrstuvwxyz', min_size=2, max_size=20),
        introduction=st.text(min_size=10, max_size=100),
        history=st.text(min_size=10, max_size=100),
        latitude=latitude_strategy,
        longitude=longitude_strategy
    )
    def test_property_4_hutong_data_completeness(self, name, introduction, history, latitude, longitude):
        """
        Property 4: Hutong Data Completeness
        *For any* hutong retrieved from the API, the response should contain all required fields:
        name, introduction, history, image, latitude, and longitude.
        **Validates: Requirements 2.1**
        """
        client = APIClient()
        
        # 清理并创建测试胡同
        Hutong.objects.all().delete()
        hutong = Hutong.objects.create(
            name=name,
            introduction=introduction,
            history=history,
            image='https://example.com/image.jpg',
            latitude=latitude,
            longitude=longitude
        )
        
        # 获取胡同概览
        response = client.get('/api/hutong/')
        assert response.status_code == 200
        
        # 验证所有必需字段存在
        data = response.data
        assert 'name' in data
        assert 'introduction' in data
        assert 'history' in data
        assert 'image' in data
        assert 'latitude' in data
        assert 'longitude' in data
        
        # 验证数据正确性
        assert data['name'] == name
        assert data['introduction'] == introduction
        assert data['history'] == history
        
        # 清理
        hutong.delete()

    @settings(max_examples=30, deadline=None)
    @given(
        name=poi_name_strategy,
        category=poi_category_strategy,
        brief=st.text(min_size=5, max_size=50),
        latitude=latitude_strategy,
        longitude=longitude_strategy
    )
    def test_property_5_poi_list_data_completeness(self, name, category, brief, latitude, longitude):
        """
        Property 5: POI List Data Completeness
        *For any* POI in the list response, the POI should contain: name, category, 
        brief description, and at least one image URL.
        **Validates: Requirements 3.1**
        """
        client = APIClient()
        
        # 清理数据
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # 创建测试胡同
        hutong = Hutong.objects.create(
            name='测试胡同',
            introduction='测试简介',
            history='测试历史',
            image='https://example.com/hutong.jpg',
            latitude=39.9,
            longitude=116.4
        )
        
        # 创建测试POI
        poi = POI.objects.create(
            name=name,
            category=category,
            description='详细描述内容',
            brief=brief,
            images=['https://example.com/poi.jpg'],
            latitude=latitude,
            longitude=longitude,
            address='测试地址',
            hutong=hutong
        )
        
        # 获取POI列表
        response = client.get('/api/pois/')
        assert response.status_code == 200
        assert len(response.data) >= 1
        
        # 验证POI数据完整性
        poi_data = response.data[0]
        assert 'name' in poi_data
        assert 'category' in poi_data
        assert 'brief' in poi_data
        assert 'images' in poi_data
        assert len(poi_data['images']) >= 1
        
        # 清理
        poi.delete()
        hutong.delete()

    @settings(max_examples=30, deadline=None)
    @given(
        name=poi_name_strategy,
        category=poi_category_strategy,
        description=st.text(min_size=10, max_size=200),
        latitude=latitude_strategy,
        longitude=longitude_strategy,
        address=st.text(min_size=5, max_size=50)
    )
    def test_property_6_poi_detail_data_completeness(self, name, category, description, latitude, longitude, address):
        """
        Property 6: POI Detail Data Completeness
        *For any* POI detail retrieved by ID, the response should contain all required fields:
        name, category, description, images, latitude, longitude, and address.
        **Validates: Requirements 3.3**
        """
        client = APIClient()
        
        # 清理数据
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # 创建测试胡同
        hutong = Hutong.objects.create(
            name='测试胡同',
            introduction='测试简介',
            history='测试历史',
            image='https://example.com/hutong.jpg',
            latitude=39.9,
            longitude=116.4
        )
        
        # 创建测试POI
        poi = POI.objects.create(
            name=name,
            category=category,
            description=description,
            brief='简介',
            images=['https://example.com/poi.jpg'],
            latitude=latitude,
            longitude=longitude,
            address=address,
            hutong=hutong
        )
        
        # 获取POI详情
        response = client.get(f'/api/pois/{poi.id}/')
        assert response.status_code == 200
        
        # 验证所有必需字段存在
        data = response.data
        assert 'name' in data
        assert 'category' in data
        assert 'description' in data
        assert 'images' in data
        assert 'latitude' in data
        assert 'longitude' in data
        assert 'address' in data
        
        # 验证数据正确性
        assert data['name'] == name
        assert data['category'] == category
        assert data['description'] == description
        
        # 清理
        poi.delete()
        hutong.delete()

    @settings(max_examples=30, deadline=None)
    @given(
        search_keyword=st.text(alphabet='abcdefghijklmnopqrstuvwxyz', min_size=2, max_size=10)
    )
    def test_property_7_search_result_relevance(self, search_keyword):
        """
        Property 7: Search Result Relevance
        *For any* search query keyword and POI in the database, if the keyword is contained 
        in the POI name (case-insensitive), then that POI should appear in the search results.
        **Validates: Requirements 3.5, 6.1**
        """
        client = APIClient()
        
        # 清理数据
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # 创建测试胡同
        hutong = Hutong.objects.create(
            name='测试胡同',
            introduction='测试简介',
            history='测试历史',
            image='https://example.com/hutong.jpg',
            latitude=39.9,
            longitude=116.4
        )
        
        # 创建包含关键词的POI
        poi_name_with_keyword = f'景点{search_keyword}店铺'
        poi = POI.objects.create(
            name=poi_name_with_keyword,
            category='shop',
            description='详细描述',
            brief='简介',
            images=['https://example.com/poi.jpg'],
            latitude=39.9,
            longitude=116.4,
            address='测试地址',
            hutong=hutong
        )
        
        # 创建不包含关键词的POI
        poi_other = POI.objects.create(
            name='其他景点',
            category='food',
            description='详细描述',
            brief='简介',
            images=['https://example.com/poi2.jpg'],
            latitude=39.9,
            longitude=116.4,
            address='测试地址2',
            hutong=hutong
        )
        
        # 搜索
        response = client.get(f'/api/pois/search/?q={search_keyword}')
        assert response.status_code == 200
        
        # 验证包含关键词的POI出现在结果中
        result_names = [p['name'] for p in response.data]
        assert poi_name_with_keyword in result_names
        
        # 验证不包含关键词的POI不在结果中（除非关键词恰好在其名称中）
        if search_keyword.lower() not in '其他景点'.lower():
            assert '其他景点' not in result_names
        
        # 清理
        poi.delete()
        poi_other.delete()
        hutong.delete()


from api.models import Route, RoutePOI


# 路线名称策略
route_name_strategy = st.text(
    alphabet='abcdefghijklmnopqrstuvwxyz中文测试',
    min_size=2,
    max_size=20
).filter(lambda x: len(x.strip()) >= 2)

# 路线时长策略（分钟）
duration_strategy = st.integers(min_value=30, max_value=180)


@pytest.mark.django_db(transaction=True)
class TestRouteProperties:
    """路线API属性测试类"""

    def setup_method(self):
        """每个测试方法前清理数据"""
        RoutePOI.objects.all().delete()
        Route.objects.all().delete()
        POI.objects.all().delete()
        Hutong.objects.all().delete()

    @settings(max_examples=30, deadline=None)
    @given(
        route_name=route_name_strategy,
        description=st.text(min_size=10, max_size=100),
        duration=duration_strategy,
        poi_count=st.integers(min_value=1, max_value=5)
    )
    def test_property_8_route_data_completeness(self, route_name, description, duration, poi_count):
        """
        Property 8: Route Data Completeness
        *For any* route in the list response, the route should contain: name, duration, and POI count.
        For route detail, it should also include description and ordered list of POIs.
        **Validates: Requirements 4.1, 4.3**
        """
        client = APIClient()
        
        # 清理数据
        RoutePOI.objects.all().delete()
        Route.objects.all().delete()
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # 创建测试胡同
        hutong = Hutong.objects.create(
            name='测试胡同',
            introduction='测试简介',
            history='测试历史',
            image='https://example.com/hutong.jpg',
            latitude=39.9,
            longitude=116.4
        )
        
        # 创建测试POIs
        pois = []
        for i in range(poi_count):
            poi = POI.objects.create(
                name=f'景点{i+1}',
                category='historic',
                description='详细描述',
                brief='简介',
                images=['https://example.com/poi.jpg'],
                latitude=39.9 + i * 0.001,
                longitude=116.4 + i * 0.001,
                address=f'测试地址{i+1}',
                hutong=hutong
            )
            pois.append(poi)
        
        # 创建测试路线
        route = Route.objects.create(
            name=route_name,
            description=description,
            duration=duration,
            hutong=hutong
        )
        
        # 创建路线-POI关联（有序）
        for i, poi in enumerate(pois):
            RoutePOI.objects.create(
                route=route,
                poi=poi,
                order=i + 1
            )
        
        # 测试路线列表API
        response_list = client.get('/api/routes/')
        assert response_list.status_code == 200
        assert len(response_list.data) >= 1
        
        # 验证列表数据完整性
        route_list_data = response_list.data[0]
        assert 'name' in route_list_data
        assert 'duration' in route_list_data
        assert 'poi_count' in route_list_data
        assert route_list_data['name'] == route_name
        assert route_list_data['duration'] == duration
        assert route_list_data['poi_count'] == poi_count
        
        # 测试路线详情API
        response_detail = client.get(f'/api/routes/{route.id}/')
        assert response_detail.status_code == 200
        
        # 验证详情数据完整性
        route_detail_data = response_detail.data
        assert 'name' in route_detail_data
        assert 'description' in route_detail_data
        assert 'duration' in route_detail_data
        assert 'poi_count' in route_detail_data
        assert 'pois' in route_detail_data
        
        # 验证数据正确性
        assert route_detail_data['name'] == route_name
        assert route_detail_data['description'] == description
        assert route_detail_data['duration'] == duration
        assert route_detail_data['poi_count'] == poi_count
        
        # 验证POI列表有序
        pois_data = route_detail_data['pois']
        assert len(pois_data) == poi_count
        for i, poi_data in enumerate(pois_data):
            assert 'id' in poi_data
            assert 'name' in poi_data
            assert 'order' in poi_data
            assert poi_data['order'] == i + 1
        
        # 清理
        RoutePOI.objects.all().delete()
        route.delete()
        for poi in pois:
            poi.delete()
        hutong.delete()


from api.models import Favorite


@pytest.mark.django_db(transaction=True)
class TestFavoriteProperties:
    """收藏API属性测试类"""

    def setup_method(self):
        """每个测试方法前清理数据"""
        Favorite.objects.all().delete()
        Token.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        RoutePOI.objects.all().delete()
        Route.objects.all().delete()
        POI.objects.all().delete()
        Hutong.objects.all().delete()

    @settings(max_examples=30, deadline=None)
    @given(
        username=username_strategy,
        password=password_strategy,
        poi_name=poi_name_strategy,
        poi_category=poi_category_strategy
    )
    def test_property_9_favorite_round_trip(self, username, password, poi_name, poi_category):
        """
        Property 9: Favorite Round-Trip
        *For any* authenticated user and POI, adding the POI to favorites then checking 
        favorites list should include that POI. Removing the POI from favorites then 
        checking favorites list should not include that POI.
        **Validates: Requirements 5.1, 5.2, 5.4**
        """
        client = APIClient()
        
        # 清理数据
        Favorite.objects.all().delete()
        User.objects.filter(username=username).delete()
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # 创建测试胡同
        hutong = Hutong.objects.create(
            name='测试胡同',
            introduction='测试简介',
            history='测试历史',
            image='https://example.com/hutong.jpg',
            latitude=39.9,
            longitude=116.4
        )
        
        # 创建测试POI
        poi = POI.objects.create(
            name=poi_name,
            category=poi_category,
            description='详细描述',
            brief='简介',
            images=['https://example.com/poi.jpg'],
            latitude=39.9,
            longitude=116.4,
            address='测试地址',
            hutong=hutong
        )
        
        # 创建测试用户并获取token
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # 添加收藏
        response_add = client.post('/api/favorites/add/', {'poi_id': poi.id})
        assert response_add.status_code in [200, 201]
        
        # 检查收藏列表应该包含该POI
        response_list = client.get('/api/favorites/')
        assert response_list.status_code == 200
        poi_ids_in_favorites = [fav['poi']['id'] for fav in response_list.data]
        assert poi.id in poi_ids_in_favorites
        
        # 删除收藏
        response_delete = client.delete(f'/api/favorites/{poi.id}/')
        assert response_delete.status_code == 200
        
        # 检查收藏列表不应该包含该POI
        response_list_after = client.get('/api/favorites/')
        assert response_list_after.status_code == 200
        poi_ids_after = [fav['poi']['id'] for fav in response_list_after.data]
        assert poi.id not in poi_ids_after
        
        # 清理
        Favorite.objects.filter(user=user).delete()
        user.delete()
        poi.delete()
        hutong.delete()

    @settings(max_examples=30, deadline=None)
    @given(
        username=username_strategy,
        password=password_strategy,
        poi_name=poi_name_strategy,
        poi_category=poi_category_strategy
    )
    def test_property_10_favorite_status_consistency(self, username, password, poi_name, poi_category):
        """
        Property 10: Favorite Status Consistency
        *For any* authenticated user and POI, the is_favorite endpoint should return true 
        if and only if the POI is in the user's favorites list.
        **Validates: Requirements 5.5**
        """
        client = APIClient()
        
        # 清理数据
        Favorite.objects.all().delete()
        User.objects.filter(username=username).delete()
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # 创建测试胡同
        hutong = Hutong.objects.create(
            name='测试胡同',
            introduction='测试简介',
            history='测试历史',
            image='https://example.com/hutong.jpg',
            latitude=39.9,
            longitude=116.4
        )
        
        # 创建测试POI
        poi = POI.objects.create(
            name=poi_name,
            category=poi_category,
            description='详细描述',
            brief='简介',
            images=['https://example.com/poi.jpg'],
            latitude=39.9,
            longitude=116.4,
            address='测试地址',
            hutong=hutong
        )
        
        # 创建测试用户并获取token
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # 初始状态：未收藏
        response_check_before = client.get(f'/api/pois/{poi.id}/is_favorite/')
        assert response_check_before.status_code == 200
        assert response_check_before.data['is_favorite'] == False
        
        # 验证收藏列表中没有该POI
        response_list_before = client.get('/api/favorites/')
        poi_ids_before = [fav['poi']['id'] for fav in response_list_before.data]
        assert poi.id not in poi_ids_before
        
        # 添加收藏
        client.post('/api/favorites/add/', {'poi_id': poi.id})
        
        # 收藏后：is_favorite应该返回true
        response_check_after = client.get(f'/api/pois/{poi.id}/is_favorite/')
        assert response_check_after.status_code == 200
        assert response_check_after.data['is_favorite'] == True
        
        # 验证收藏列表中有该POI
        response_list_after = client.get('/api/favorites/')
        poi_ids_after = [fav['poi']['id'] for fav in response_list_after.data]
        assert poi.id in poi_ids_after
        
        # 删除收藏
        client.delete(f'/api/favorites/{poi.id}/')
        
        # 删除后：is_favorite应该返回false
        response_check_final = client.get(f'/api/pois/{poi.id}/is_favorite/')
        assert response_check_final.status_code == 200
        assert response_check_final.data['is_favorite'] == False
        
        # 清理
        Favorite.objects.filter(user=user).delete()
        user.delete()
        poi.delete()
        hutong.delete()

    @settings(max_examples=30, deadline=None)
    @given(
        poi_name=poi_name_strategy,
        poi_category=poi_category_strategy
    )
    def test_property_11_authentication_required_for_protected_endpoints(self, poi_name, poi_category):
        """
        Property 11: Authentication Required for Protected Endpoints
        *For any* request to a protected endpoint (favorites operations) without a valid token, 
        the system should reject the request with 401 Unauthorized.
        **Validates: Requirements 5.3, 8.4**
        """
        client = APIClient()
        
        # 清理数据
        POI.objects.all().delete()
        Hutong.objects.all().delete()
        
        # 创建测试胡同
        hutong = Hutong.objects.create(
            name='测试胡同',
            introduction='测试简介',
            history='测试历史',
            image='https://example.com/hutong.jpg',
            latitude=39.9,
            longitude=116.4
        )
        
        # 创建测试POI
        poi = POI.objects.create(
            name=poi_name,
            category=poi_category,
            description='详细描述',
            brief='简介',
            images=['https://example.com/poi.jpg'],
            latitude=39.9,
            longitude=116.4,
            address='测试地址',
            hutong=hutong
        )
        
        # 不提供认证token，测试所有受保护的端点
        
        # 测试获取收藏列表（需要认证）
        response_list = client.get('/api/favorites/')
        assert response_list.status_code == 401
        
        # 测试添加收藏（需要认证）
        response_add = client.post('/api/favorites/add/', {'poi_id': poi.id})
        assert response_add.status_code == 401
        
        # 测试删除收藏（需要认证）
        response_delete = client.delete(f'/api/favorites/{poi.id}/')
        assert response_delete.status_code == 401
        
        # 测试检查是否已收藏（需要认证）
        response_check = client.get(f'/api/pois/{poi.id}/is_favorite/')
        assert response_check.status_code == 401
        
        # 测试使用无效token
        client.credentials(HTTP_AUTHORIZATION='Token invalid_token_12345')
        
        response_list_invalid = client.get('/api/favorites/')
        assert response_list_invalid.status_code == 401
        
        response_add_invalid = client.post('/api/favorites/add/', {'poi_id': poi.id})
        assert response_add_invalid.status_code == 401
        
        # 清理
        poi.delete()
        hutong.delete()
