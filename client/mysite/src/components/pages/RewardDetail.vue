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
                <v-card-text class="my-2">レアリティ：{{ rarityStr }}</v-card-text>
                <v-img
                    :src="detailData.image_url"
                    :class="'rarity-' + detailData.fields.rarity"
                    class="my-3 mx-auto image-frame"
                    height="200px"
                >
                </v-img>
                <audio
                    class="mx-auto"
                    controls
                    controlslist="nodownload"
                    :src="detailData.audio_url">
                </audio>
                <v-card-text class="my-3">{{ detailData.fields.reward_content }}</v-card-text>
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
            detailData: {},
            rarityStr: '',
            rarityArr: [
                {"id": 1, "rarityName": "ノーマル（N）", "value": 1},
                {"id": 2, "rarityName": "レア（R）", "value": 2},
                {"id": 3, "rarityName": "スーパーレア（SR）", "value": 3},
                {"id": 4, "rarityName": "ウルトラレア（UR）", "value": 4}
            ]
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

            // レアリティ表記整形
            let rarityInt = this.detailData.fields.rarity;
            let resultObj = this.rarityArr.filter(rarity => rarity.value == rarityInt);
            this.rarityStr = resultObj[0].rarityName;
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
    .rarity-1 {
        border: solid 2px #8b4513;
    }
    .rarity-2 {
        border: solid 2px #fff;
        border-image: linear-gradient(45deg, #757575 0%, #9E9E9E 45%, #E8E8E8 70%, #9E9E9E 85%, #757575 90% 100%);
        border-image-slice: 1;
    }
    .rarity-3 {
        border: solid 2px #fff;
        border-image: linear-gradient(45deg, #B67B03 0%, #DAAF08 45%, #FEE9A0 70%, #DAAF08 85%, #B67B03 90% 100%);
        border-image-slice: 1;
    }
    .rarity-4 {
        border: solid 2px #fff;
        border-image: conic-gradient(#f5f551,#5eff5e,#84a1ff,#ff45ff,#ff5a5a,#ffbc41,#f5f551) 1;
        border-image-slice: 1;
    }
    .image-frame {
        width: 400px;
    }
</style>