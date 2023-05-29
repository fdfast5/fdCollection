from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

from .twitch_api import twitch_return
from .models import User, Reward, Collection
from .serializers import UserSerializer, RewardSerializer, CollectionSerializer
# Create your views here.

# 管理画面、報酬リスト取得
class RewardList(generics.ListAPIView):
    serializer_class = RewardSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        params = [
            {
                'id': 1,
                'title': 'テストデータ'
            }
        ]
        return JsonResponse(params, safe=False)
        

# 管理画面、報酬編集
class RewardRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

# ユーザーログイン後、ユーザー取得（登録）
class UserListCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        # クエリパラメータからTwitch APIで使用するアクセストークンを取得
        access_token = request.query_params.get('access_token')

        # TwitchAPIで連携したユーザー情報を取得
        twitch = twitch_return(access_token)
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