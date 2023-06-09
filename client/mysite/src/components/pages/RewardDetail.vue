<template>
    <v-row justify="center">
        <v-dialog
            v-model="rewardDialog"
            :persistent='true'
            width="70%"
            height="100%"
            no-click-animation
            >
            <v-card class="pa-3">
                <v-card-title class="card-title-frame">
                    <span class="card-title">{{ detailData.fields.reward_title }}</span>
                </v-card-title>
                    <v-img
                        :src="detailData.url"
                        class="white--text align-end"
                        height="200px"
                    >
                    </v-img>
                    <v-card-text>{{ detailData.fields.reward_content }}</v-card-text>
                    <v-btn
                        @click="closeDialog()"
                    >
                        閉じる
                    </v-btn>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>

export default {
    props: [
        'dialog',
        'field'
    ],
    data () {
        return {
            detailData: {}
        };
    },
    computed: {
        rewardDialog: {
            get () {
                return this.dialog;
            }
        }
    },
    watch: {
        dialog() {
            // ダイアログが開かれたら対象報酬データ受け取り
            if (this.dialog) {
                this.getRewardDetail();
            }
        }
    },
    methods: {
        /** -------------------------------------
         * 報酬内容取得
         * ------------------------------------ */
        getRewardDetail() {
            this.detailData = this.field;
        },
        /** ----------------------------------------------
         * このダイアログを閉じる処理
         * ---------------------------------------------- */
        closeDialog () {
            this.$emit('close');
        }
    }
};
</script>

<style scoped>
    .card-title-frame {
        background-color: #424242;
        border-radius: 4px;
    }
    .card-title {
        color: #fff;
    }
</style>