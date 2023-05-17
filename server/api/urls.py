from django.urls import path
from .views import *

urlpatterns = [
    path('reward/', RewardList.as_view()),
    path('reward/<pk>/', RewardRetrieveUpdate.as_view()),

    path('user/', UserListCreate.as_view()),

    path('collection/', CollectionListCreate.as_view())
]