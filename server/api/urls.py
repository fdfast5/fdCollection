from django.urls import path
from .views import *

urlpatterns = [
    path('reward/', RewardList.as_view()),

    path('user/', UserListCreate.as_view()),

    path('image/', ImageCreate.as_view()),

    path('audio/', AudioCreate.as_view())
]