from django.shortcuts import render
from rest_framework import generics

from .models import User, Reward, Collection
from .serializers import UserSerializer, RewardSerializer, CollectionSerializer
# Create your views here.

# 管理画面、報酬リスト取得
class RewardList(generics.ListAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

# 管理画面、報酬編集
class RewardRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

# ユーザーログイン後、ユーザー取得（登録）
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# コレクション取得（登録）
class CollectionListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CollectionSerializer