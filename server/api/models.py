from django.db import models

# Create your models here.
# ユーザーマスタ
class User(models.Model):
    twitch_user_id  = models.CharField(max_length=10)
    user_login      = models.CharField(max_length=256)
    user_name       = models.CharField(max_length=256, null=True)
    valid_flag      = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

# 報酬マスタ
class Reward(models.Model):
    twitch_reward_id    = models.CharField(max_length=256)
    reward_title        = models.CharField(max_length=256)
    reward_parent_flag  = models.BooleanField()
    reward_parent_id    = models.IntegerField(null=True)
    reward_content      = models.CharField(max_length=256, null=True)
    reward_img_path     = models.CharField(max_length=256, null=True)
    reward_audio_path   = models.CharField(max_length=256, null=True)
    rarity              = models.IntegerField(null=True)
    valid_flag          = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reward'

# コレクションテーブル
class Collection(models.Model):
    twitch_user_id      = models.CharField(max_length=10)
    twitch_reward_id    = models.CharField(max_length=256)
    get_date            = models.DateTimeField()
    valid_flag          = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'collection'

# 画像テーブル
class Image(models.Model):
    twitch_reward_id    = models.CharField(max_length=10)
    image_file_name     = models.ImageField(upload_to="image/", null=True)
    valid_flag          = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image'    

# 音声テーブル  
class Audio(models.Model):
    twitch_reward_id    = models.CharField(max_length=10)
    audio_file_name     = models.FileField(upload_to="audio/", null=True)
    valid_flag          = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audio'