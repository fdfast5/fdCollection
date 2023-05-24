<template>
    <v-container>
        <v-btn class="pink white--text" @click="twitchLogin">Twitch Login</v-btn>
    </v-container>
</template>

<script>
import axios from 'axios';
import router from "../../router";
export default {
    name: "fd-collection-login",
    data: () => ({
        params: {}
    }),
    mounted() {
        this.userCheck(location.hash);
    },
    methods: {
        /** --------------------------------------
         * Twitch連携（Twitch内でログインを行う）
         * リダイレクト時、access_tokenを取得
         * ------------------------------------- */
        twitchLogin() {
            let client_id = process.env.VUE_APP_CLIENT_ID; // envで保持
            let redirect_uri = process.env.VUE_APP_REDIRECT_URL; // envで保持
            window.location.href = 'https://id.twitch.tv/oauth2/authorize?client_id=' + client_id + '&redirect_uri=' + encodeURIComponent(redirect_uri) + '&response_type=token'
        },
        /** ---------------------------------
         * Twitch連携ユーザーチェック
         * --------------------------------*/
        userCheck(hash) {
            if (hash) {
                // Twitch連携後のリダイレクトでアクセストークンがあるかチェック
                const result = location.hash.match(/access_token=(.*)&scope/);
                if (result) {
                    // アクセストークンがあれば
                    // Twitch API: ユーザー情報を取得
                    // DB: ユーザー情報がなければDB登録し、ユーザーIDを返却
                    const token = result[1];
                    this.params.access_token = token;
                    axios.get(
                        'http://localhost:8000/api/user/',
                        { params: this.params }
                    )
                    .then(
                        res => {
                            // TwitchユーザーID保持
                            sessionStorage.setItem('twitchUserId', res.data.user_id);
                            // 処理が正常終了したら、コレクション画面へ遷移
                            router.push('/collectionlist');
                        }
                    )
                    .catch(
                        e => {
                            alert(e);
                        }
                    )
                }
            }
        }
    }
};
</script>