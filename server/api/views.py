from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.core.serializers import serialize
import json

from .twitch_api import twitch_return
from .models import User, Reward, Collection, Image, Audio
from .serializers import UserSerializer, RewardSerializer, ImageSerializer, AudioSerializer
# Create your views here.

# 管理画面、報酬リスト取得、更新
class RewardList(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # クエリパラメータからTwitch APIで使用するアクセストークンがあれば
        # TwitchAPIから報酬リストを取得
        if request.query_params.get('access_token'):
            access_token = request.query_params.get('access_token')
            user_info = twitch_return(access_token, 'user', None)
            user_id = user_info.id
            # 報酬リスト
            twitch = twitch_return(access_token, 'reward', user_id)
            # 報酬引き換えリスト
            # collection = twitch_return(access_token, 'history', user_id)
        
        # クエリパラメータにユーザー画面からのアクセスを判断するフラグがあれば親報酬のみ取得
        # 親ガチャリスト画面
        if request.query_params.get('user_access'):
            res = Reward.objects.filter(reward_parent_flag=True)
            count = Reward.objects.filter(reward_parent_flag=True).count()
        # ガチャ毎報酬一覧画面
        elif request.query_params.get('parent_id'):
            user_id = request.query_params.get('user_id')
            parent_id = request.query_params.get('parent_id')
            offset = request.query_params.get('offset')
            limit = request.query_params.get('limit')

            res = Reward.objects.filter(reward_parent_id=parent_id).all()[int(offset):int(limit)]
            count = Reward.objects.filter(reward_parent_id=parent_id).count()
            collectionRes = Collection.objects.filter(twitch_user_id=user_id)
        else:
            res = Reward.objects.all()
            count = Reward.objects.all().count()
        
        serialized_data = serialize("json", res)
        reward_list = json.loads(serialized_data)

        # 対象ガチャ報酬一覧画面の場合、表示/非表示データ整形
        if request.query_params.get('parent_id'):
            collection_serialize = serialize("json", collectionRes)
            collection_list = json.loads(collection_serialize)

            for name in reward_list:
                # Collectionテーブルに対象ユーザーのデータがなければ全て非表示
                if not collection_list:
                    name['close_flag'] = True
                else:
                    name['close_flag'] = True

                    # Collectionテーブルに対象データのtwitch_reward_idが一致したら表示させる
                    for collection_name in collection_list:
                        if collection_name['fields']['twitch_reward_id'] == name['fields']['twitch_reward_id']:
                            name['close_flag'] = False
                            break
                # レコード数追加
                name['count'] = count
                # 画像URL追加
                # データがなければロック画像
                if name['close_flag'] == True:
                    name['image_url'] = 'http://localhost:8000/media/istockphoto-936681148-1024x1024.jpg'
                else:
                    name['image_url'] = 'http://localhost:8000' + str(name['fields']['reward_img_path'])
                # 音声URL整形
                name['audio_url'] = 'http://localhost:8000' + str(name['fields']['reward_audio_path'])

        return JsonResponse(reward_list, safe=False)
    
    def post(self, request):
        data = request.data
        pk = data['id']
        reward_title = data['reward_title']
        reward_parent_flag = data['reward_parent_flag']
        reward_parent_id = data['reward_parent_id']
        reward_content = data['reward_content']
        reward_img_path = data['reward_img_path']
        reward_audio_path = data['reward_audio_path']
        rarity = data['rarity']
        valid_flag = data['valid_flag']

        Reward.objects.filter(pk=pk).update(
            reward_title = reward_title,
            reward_parent_flag = reward_parent_flag,
            reward_parent_id = reward_parent_id,
            reward_content = reward_content,
            reward_img_path = reward_img_path,
            reward_audio_path = reward_audio_path,
            rarity = rarity,
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
        twitch = twitch_return(access_token, 'user', None)
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

# 音声アップロード
class AudioCreate(generics.ListCreateAPIView):
    serializer_class = AudioSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        twitch_reward_id = data['twitch_reward_id']
        audio_data = data['audio_data']
        if audio_data is not None:
            audio = Audio.objects.create(
                twitch_reward_id = twitch_reward_id,
                audio_file_name = audio_data
            )

            params = {
                'url': audio.audio_file_name.url,
                'status': True
            }
            return JsonResponse(params)
        
        params = {
            'url': '',
            'status': False
        }
        return JsonResponse(params)