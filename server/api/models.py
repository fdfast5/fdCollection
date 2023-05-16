from django.db import models

# Create your models here.
class User(models.Model):
    user_id         = models.BigAutoField
    twitch_user_id  = models.CharField(max_length=10)
    user_login      = models.CharField(max_length=256)
    user_name       = models.CharField(max_length=256, null=True)
    valid_flag      = models.BooleanField(default=True)
    created_at      = models.DateTimeField()
    updated_at      = models.DateTimeField()

    class Meta:
        db_table = 'user'