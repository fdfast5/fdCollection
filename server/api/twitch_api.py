from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio
import environ

env = environ.Env()
env.read_env('.env')

async def twitch_example(access_token, select_api):
    app_id = env('TWITCH_APP_ID')
    app_secret = env('TWITCH_APP_SECRET')
    #Twitch developersで取得したクライアントIDとシークレットキーを入力する
    twitch = await Twitch(app_id, app_secret)
    await twitch.set_user_authentication(access_token, [], access_token)

    if select_api == 'user':
        result = await first(twitch.get_users())
    elif select_api == 'reward':
        result = await twtich.get_custom_reward()
    #ユーザー情報を取得する
    await twitch.close()
    return result

async def main(access_token, select_api):
    coro = twitch_example(access_token, select_api)
    value = await coro
    return value

def twitch_return(access_token, select_api):
    return asyncio.run(main(access_token, select_api))