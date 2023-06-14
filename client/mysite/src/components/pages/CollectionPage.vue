<template>
  <v-app>
    <v-container fluid>
      <div class="text-h2 font-weight-bold d-flex justify-center mb-3">fd-collection</div>
      <v-row v-if="desserts.length > 0" class="collection-list">
        <v-col
          v-for="item in desserts"
          :key="item.pk"
          cols="12"
          md="4"
        >
          <v-card
            :disabled="item.close_flag"
            @click="openRewardDetail(item)">
            <v-img
              :src="item.image_url"
              class="white--text align-end"
              height="200px"
            >
            </v-img>
          </v-card>
        </v-col>
      </v-row>
      <v-row v-else>
        <div class="text-h4 mx-auto my-4">{{ errorMessage }}</div>
      </v-row>
      <v-pagination
        v-model="page"
        :length="pageCount"
        @click="clickPagination()"
      ></v-pagination>
    </v-container>
    <RewardDetail
      :dialog="rewardDetailDialog"
      :field="rewardDetailData"
      @close="closeRewardDetail"
    />
  </v-app>
</template>

<script>
import axios from 'axios';
import RewardDetail from './RewardDetail';
export default {
    name: "fd-collection-page",
    components: {
      RewardDetail
    },
    data: () => ({
        desserts: [],
        params: {},
        offset: 0,
        limit: 9,
        page: 1,
        pageCount: 0,
        rewardDetailDialog: false,
        rewardDetailData: null,
        errorMessage: ''
    }),
    mounted() {
        this.getCapsuleToys();
    },
    methods: {
        /** ----------------------------
         * ガチャ子一覧取得
         * ----------------------------- */
        getCapsuleToys() {
            this.params.user_id = sessionStorage.getItem('twitchUserId');
            this.params.parent_id = sessionStorage.getItem('rewardParentPk');
            this.params.offset = this.offset;
            this.params.limit = this.limit;
            axios.get(
                'http://localhost:8000/api/reward/',
                { params: this.params }
            )
            .then(
                res => {
                    this.desserts = res.data;
                    if (this.desserts.length > 0) {
                      let count = this.desserts[0].count;
                      this.pageCount = Math.ceil(count / 9);
                    } else {
                      this.errorMessage = '現在準備中'
                    }
                    
                }
            )
            .catch(
                e => {
                    alert(e);
                }
            )
        },
        clickPagination() {
            this.offset = this.page * 9 - 9;
            this.limit = this.page * 9;
            this.getCapsuleToys();
        },
        openRewardDetail(item) {
          this.rewardDetailDialog = true;
          this.rewardDetailData = item;
        },
        closeRewardDetail() {
          this.rewardDetailDialog = false;
        }
    }
};
</script>

<style scoped>
    .collection-list {
        margin: auto;
        max-width: 80%;
    }
</style>