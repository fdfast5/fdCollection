from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio
import environ

env = environ.Env()
env.read_env('.env')

async def twitch_example(access_token):
    app_id = env('TWITCH_APP_ID')
    app_secret = env('TWITCH_APP_SECRET')
    #Twitch developersで取得したクライアントIDとシークレットキーを入力する
    twitch = await Twitch(app_id, app_secret)
    await twitch.set_user_authentication(access_token, [], access_token)
    #自身のTwitchユーザー名を入力
    #ここは表示名ではないことに注意
    user = await first(twitch.get_users())
    #ユーザー情報を取得する
    await twitch.close()
    return user

async def main(access_token):
    coro = twitch_example(access_token)
    value = await coro
    return value

def twitch_return(access_token):
    return asyncio.run(main(access_token))