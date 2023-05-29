<template>
    <v-app>
        <v-app-bar
            color="blue-grey"
            dark app height="50">fd-collection管理画面
        </v-app-bar>
        <v-card
            class="mx-4 mt-16">
            <v-table>
                <thead>
                    <tr>
                        <th class="text-left">
                        タイトル
                        </th>
                        <th class="text-left">
                        詳細
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr
                        v-for="item in desserts"
                        :key="item.id"
                    >
                        <td>{{ item.title }}</td>
                        <td>ボタン</td>
                    </tr>
                </tbody>
            </v-table>
        </v-card>
    </v-app>
</template>

<script>
import axios from 'axios';
import router from "../../router";
export default {
    name: "fd-collection",
    data: () => ({
        desserts: [
        //   {
        //     id: 1,
        //     title: '黄猿',
        //   },
        //   {
        //     id: 2,
        //     title: '聖徳太子',
        //   },
        ]
    }),
    mounted() {
        this.checkLoggedIn();
    },
    methods: {
        /** -------------------------
         * ログインチェック
         * ----------------------- */
        checkLoggedIn() {
            // tokenがなければログイン画面へ遷移
            if (!sessionStorage.getItem('token')) {
                router.push("/auth");
            } else {
                // 報酬リスト取得
                this.getReward();
            }
        },
        /** ----------------------
         * 報酬リスト取得
         * -------------------- */
        getReward() {
            // Twitch API: 報酬リストを取得
            // DB: Twitch内の報酬がDBになければ追加し、rewardテーブルデータを返却
            axios.get(
                'http://localhost:8000/api/reward'
            )
            .then(
                res => {
                    this.desserts = res.data;
                }
            )
            .catch(
                e => {
                    alert(e);
                }
            )
        }
    }
};
</script>