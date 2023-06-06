<template>
    <v-app>
        <v-app-bar
            color="blue-grey"
            dark app height="50"
            class="pl-3">fd-collection管理画面
        </v-app-bar>
        <v-card
            class="mx-4 mt-16">
            <v-table>
                <thead>
                    <tr>
                        <th class="text-left">
                        タイトル
                        </th>
                        <th>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr
                        v-for="item in desserts"
                        :key="item.pk"
                    >
                        <td>{{ item.fields.reward_title }}</td>
                        <td>
                            <v-btn
                                @click="openDetail(item.fields, item.pk)"
                            >
                                詳細
                            </v-btn>
                        </td>
                    </tr>
                </tbody>
            </v-table>
        </v-card>
        <CollectionDetail
            :dialog="collectionDetailDialog"
            :field="collectionDetailData"
            :pk="collectionDetailPk"
            @close="closeDetail"
        />
    </v-app>
</template>

<script>
import axios from 'axios';
import router from "../../router";
import CollectionDetail from './CollectionDetail';
export default {
    name: "fd-collection",
    components: {
        CollectionDetail
    },
    data: () => ({
        desserts: [],
        params: {},
        collectionDetailDialog: false,
        collectionDetailData: null,
        CollectionDetailPk: null
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
            // Twitch連携後のリダイレクトでアクセストークンがあるかチェック
            const result = location.hash.match(/access_token=(.*)&scope/);
            if (result) {
                // アクセストークンがあれば
                // Twitch API: 報酬リストを取得し最新情報に更新
                const token = result[1];
                this.params.access_token = token;
            }
            // DB: Twitch内の報酬がDBになければ追加し、rewardテーブルデータを返却
            axios.get(
                'http://localhost:8000/api/reward',
                { params: this.params }
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
        },
        /** ----------------------
         * 詳細ダイアログを開く
         * -------------------- */
        openDetail(field, pk) {
            this.collectionDetailDialog = true;
            this.collectionDetailData = field;
            this.collectionDetailPk = pk;
        },
        /** ----------------------
         * 詳細ダイアログを閉じる
         * -------------------- */
        closeDetail() {
            this.collectionDetailDialog = false;
        }
    }
};
</script>