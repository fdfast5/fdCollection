<template>
    <v-container fluid>
      <div class="text-h2 font-weight-bold d-flex justify-center mb-3">fd-collection</div>
      <v-row dense>
        <v-col
          v-for="item in desserts"
          :key="item.pk"
          cols="12"
          sm="6"
        >
          <v-card
            @click="selectCollection(item.pk)">
            <v-img
              :src="item.fields.url"
              class="white--text align-end"
              height="200px"
            >
              <v-card-title v-text="item.fields.reward_title"></v-card-title>
            </v-img>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';
import router from "../../router";
export default {
    name: "fd-collection-list",
    data: () => ({
        desserts: [],
        params: {}
    }),
    mounted() {
        this.getCapsuleToyMachines();
    },
    methods: {
        /** ----------------------------
         * コレクション選択
         * ----------------------------- */
        selectCollection(id) {
            sessionStorage.setItem('rewardParentPk', id);
            router.push('/collectionpage');
        },
        /** ----------------------------
         * 親ガチャ一覧取得
         * ----------------------------- */
        getCapsuleToyMachines() {
            this.params.user_access = true;
            axios.get(
                'http://localhost:8000/api/reward/',
                { params: this.params }
            )
            .then(
                res => {
                    this.desserts = res.data;

                    Object.values(this.desserts).forEach(key => {
                        // 画像表示URL
                        key.fields.url = 'http://localhost:8000' + key.fields.reward_img_path;
                    })
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