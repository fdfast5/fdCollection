<template>
    <v-row justify="center">
        <v-dialog
            v-model="collectionDialog"
            :persistent='true'
            width="70%"
            height="100%"
            no-click-animation
            >
            <v-card class="pa-3">
                <v-card-title>詳細</v-card-title>
                    <v-form>
                        <v-container>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>タイトル</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-text-field
                                        v-model="detailData.reward_title"
                                    />
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>親報酬フラグ</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-checkbox v-model="detailData.reward_parent_flag" label="親として持つ" />
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>親報酬ID</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-text-field
                                        v-model="detailData.reward_parent_id"
                                    />
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>報酬内容</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-text-field
                                        v-model="detailData.reward_content"
                                    />
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>報酬画像</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-text-field
                                        v-model="detailData.reward_img_path"
                                    />
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>報酬音声</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-text-field
                                        v-model="detailData.reward_audio_path"
                                    />
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>有効フラグ</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-checkbox v-model="detailData.valid_flag" label="有効フラグ" />
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-form>
                    <v-btn
                        @click="updateDetailData()"
                    >
                        保存
                    </v-btn>
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

import axios from 'axios';

export default {
    props: [
        'dialog',
        'field',
        'pk'
    ],
    data () {
        return {
            detailTitle: '詳細',
            detailData: {},
            detailPk: null
        };
    },
    computed: {
        collectionDialog: {
            get () {
                return this.dialog;
            }
        }
    },
    watch: {
        dialog() {
            // ダイアログが開かれたら対象報酬データ受け取り
            if (this.dialog) {
                this.getCollectionDetail();
            }
        }
    },
    methods: {
        /** -------------------------------------
         * 報酬内容取得
         * ------------------------------------ */
        getCollectionDetail() {
            this.detailData = this.field;
            this.detailPk = this.pk;
        },
        /** -------------------------------------
         * 報酬内容更新
         * ------------------------------------ */
        updateDetailData() {
            axios.post(
                'http://localhost:8000/api/reward/',
                {
                    id: this.detailPk,
                    reward_title: this.detailData.reward_title,
                    reward_parent_flag: this.detailData.reward_parent_flag,
                    reward_parent_id: this.detailData.reward_parent_id,
                    reward_content: this.detailData.reward_content,
                    valid_flag: this.detailData.valid_flag
                }
            )
            .then(
                res => {
                    console.log(JSON.stringify(res.data, null, 2));
                }
            )
            .catch(
                e => {
                    alert(e);
                }
            )
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
