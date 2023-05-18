from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio

async def twitch_example(access_token):
    app_id = 'kfka7cipofpyncxov9lrhu0l6qnmjx'
    app_secret = 'wxitlteic087gzag4wg0o2g40miy1a'
    #Twitch developersで取得したクライアントIDとシークレットキーを入力する
    twitch = await Twitch(app_id, app_secret)
    await twitch.set_user_authentication(access_token, [], access_token)
    #自身のTwitchユーザー名を入力
    #ここは表示名ではないことに注意
    user = await first(twitch.get_users())
    #ユーザーidを取得する
    await twitch.close()
    return user

async def main(access_token):
    coro = twitch_example(access_token)
    value = await coro
    return value

def twitch_return(access_token):
    return asyncio.run(main(access_token))