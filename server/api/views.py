from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.core.serializers import serialize
import json

from .twitch_api import twitch_return
from .models import User, Reward, Collection, Image
from .serializers import UserSerializer, RewardSerializer, CollectionSerializer, ImageSerializer
# Create your views here.

# 管理画面、報酬リスト取得、更新
class RewardList(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # クエリパラメータからTwitch APIで使用するアクセストークンがあれば
        # TwitchAPIから報酬リストを取得
        if request.query_params.get('access_token'):
            access_token = request.query_params.get('access_token')
            twitch = twitch_return(access_token, 'reward')
            # print(twitch)
        
        res = Reward.objects.all()
        serialized_data = serialize("json", res)
        reward_list = json.loads(serialized_data)

        return JsonResponse(reward_list, safe=False)
    
    def post(self, request):
        data = request.data
        pk = data['id']
        reward_title = data['reward_title']
        reward_parent_flag = data['reward_parent_flag']
        reward_parent_id = data['reward_parent_id']
        reward_content = data['reward_content']
        reward_img_path = data['reward_img_path']
        valid_flag = data['valid_flag']

        Reward.objects.filter(pk=pk).update(
            reward_title = reward_title,
            reward_parent_flag = reward_parent_flag,
            reward_parent_id = reward_parent_id,
            reward_content = reward_content,
            reward_img_path = reward_img_path,
            valid_flag = valid_flag
        )

        params = {
            'id': pk
        }
        return JsonResponse(params)

# ユーザーログイン後、ユーザー取得（登録）
class UserListCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        # クエリパラメータからTwitch APIで使用するアクセストークンを取得
        access_token = request.query_params.get('access_token')

        # TwitchAPIで連携したユーザー情報を取得
        twitch = twitch_return(access_token, 'user')
        # Twitch連携一意ユーザーID
        res_user_id = twitch.id
        # Twitch連携ログインID
        res_user_login = twitch.login
        # Twitch連携表示名
        res_user_name = twitch.display_name
        # 対象IDがDB内のユーザーマスタに存在するか判定
        db_check = User.objects.filter(twitch_user_id=res_user_id).exists()
        # 存在しない場合（初回連携の場合）DB登録
        if not db_check:
            User.objects.create(
                twitch_user_id = res_user_id,
                user_login = res_user_login,
                user_name = res_user_name,
                valid_flag = 1
            )
        
        params = {
            'user_id': res_user_id,
        }
        return JsonResponse(params)

# コレクション取得（登録）
class CollectionListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CollectionSerializer

# 画像アップロード
class ImageCreate(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        twitch_reward_id = data['twitch_reward_id']
        image_data = data['image_data']
        if image_data is not None:
            img = Image.objects.create(
                twitch_reward_id = twitch_reward_id,
                image_file_name = image_data
            )

            params = {
                'url': img.image_file_name.url,
                'status': True
            }
            return JsonResponse(params)
        
        params = {
            'url': '',
            'status': False
        }
        return JsonResponse(params)