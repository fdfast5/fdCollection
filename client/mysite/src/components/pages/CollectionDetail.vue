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
                <v-card-title class="card-title-frame">
                    <span class="card-title">詳細</span>
                </v-card-title>
                    <v-form>
                        <v-container>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>TwitchID</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-text-field
                                        readonly
                                        v-model="detailData.twitch_reward_id"
                                    />
                                </v-col>
                            </v-row>
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
                                    <div>レアリティ</div>
                                </v-col>
                                <v-col cols="8">
                                    <v-radio-group
                                        v-model="detailData.rarity"
                                    >
                                        <v-radio
                                            v-for="flag in raritySelectBox"
                                            :key="flag.id"
                                            :label="flag.rarityName"
                                            :value="flag.value"
                                        />
                                    </v-radio-group>
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
                                <v-col cols="4">
                                    <v-text-field
                                        readonly
                                        v-model="detailData.reward_img_path"
                                    />
                                </v-col>
                                <v-col cols="4">
                                    <input
                                        style="display: none"
                                        accept=".jpg,.png,.image"
                                        type="file"
                                        ref="imageInput"
                                        v-on:change="fileSelected"
                                    />
                                    <v-btn class="ml-3" color="primary" @click="imgBtnClick">画像選択</v-btn>
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col cols="4">
                                    <div>報酬音声</div>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-field
                                        readonly
                                        v-model="detailData.reward_audio_path"
                                    />
                                </v-col>
                                <v-col cols="4">
                                    <input
                                        style="display: none"
                                        accept=".mp3"
                                        type="file"
                                        ref="audioInput"
                                        v-on:change="audioFileSelected"
                                    />
                                    <v-btn class="ml-3" color="primary" @click="audioBtnClick">音声選択</v-btn>
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
                        class="mb-4"
                        @click="confirm()"
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
        <ConfirmDialog
            :open="confirmDialog"
            @cancel="confirmDialog = !confirmDialog"
            @save="updateDetailData"
        />
    </v-row>
</template>

<script>
import ConfirmDialog from './ConfirmDialog';
import axios from 'axios';

export default {
    props: [
        'dialog',
        'field',
        'pk'
    ],
    components: {
        ConfirmDialog
    },
    data () {
        return {
            detailTitle: '詳細',
            detailData: {},
            detailPk: null,
            fileInfo: '',
            audioFileInfo: '',
            confirmDialog: false,
            error: '',
            raritySelectBox: [
                {"id": 1, "rarityName": "ノーマル（N）", "value": 1},
                {"id": 2, "rarityName": "レア（R）", "value": 2},
                {"id": 3, "rarityName": "スーパーレア（SR）", "value": 3},
                {"id": 4, "rarityName": "ウルトラレア（UR）", "value": 4}
            ]
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
        imgBtnClick () {
            this.$refs.imageInput.click();
        },
        audioBtnClick () {
            this.$refs.audioInput.click();
        },
        /** ----------------------------------------------
         * 画像選択時に常に画像を取得
         * ---------------------------------------------- */
        fileSelected (event) {
            this.fileInfo = event.target.files[0];
            const files = this.$refs.imageInput.files[0];
            if (!files) {
                return;
            }
            this.detailData.reward_img_path = files.name;
        },
        /** ----------------------------------------------
         * 音声選択時に常に音声を取得
         * ---------------------------------------------- */
        audioFileSelected (event) {
            this.audioFileInfo = event.target.files[0];
            const files = this.$refs.audioInput.files[0];
            if (!files) {
                return;
            }
            this.detailData.reward_audio_path = files.name;
        },
        confirm() {
            this.confirmDialog = true;
        },
        /** ----------------------------------------------
         * 画像アップロード
         * ---------------------------------------------- */
        async FileUpload () {
            const formData = new FormData();
            formData.append('image_data', this.fileInfo);
            formData.append('twitch_reward_id', this.detailData.twitch_reward_id);
    
            await axios.post(
                'http://localhost:8000/api/image/', formData
            )
            .then(res => {
                if (res.data.status) {
                    this.detailData.reward_img_path = res.data.url;
                }
            })
            .catch(e => {
                this.error = e;
            })
        },
        /** ----------------------------------------------
         * 音声アップロード
         * ---------------------------------------------- */
        async audioFileUpload () {
            const formData = new FormData();
            formData.append('audio_data', this.audioFileInfo);
            formData.append('twitch_reward_id', this.detailData.twitch_reward_id);
    
            await axios.post(
                'http://localhost:8000/api/audio/', formData
            )
            .then(res => {
                if (res.data.status) {
                    this.detailData.reward_audio_path = res.data.url;
                }
            })
            .catch(e => {
                this.error = e;
            })
        },
        /** -------------------------------------
         * 報酬内容更新
         * ------------------------------------ */
        async updateDetailData() {
            if (this.fileInfo) {
                await this.FileUpload();
            }
            if (this.audioFileInfo) {
                await this.audioFileUpload();
            }
            await axios.post(
                'http://localhost:8000/api/reward/',
                {
                    id: this.detailPk,
                    reward_title: this.detailData.reward_title,
                    reward_parent_flag: this.detailData.reward_parent_flag,
                    reward_parent_id: this.detailData.reward_parent_id,
                    reward_content: this.detailData.reward_content,
                    reward_img_path: this.detailData.reward_img_path,
                    reward_audio_path: this.detailData.reward_audio_path,
                    rarity: this.detailData.rarity,
                    valid_flag: this.detailData.valid_flag
                }
            )
            .then(
                res => {
                    this.detailData = {};
                    if (res.data) {
                        //確認ダイアログ閉じる
                        this.confirmDialog = false;
                        //詳細ダイアログ閉じる
                        this.$emit('close');
                    }
                }
            )
            .catch(
                e => {
                    this.detailData = {};
                    alert(e);
                }
            )
        },
        /** ----------------------------------------------
         * このダイアログを閉じる処理
         * ---------------------------------------------- */
        closeDialog () {
            this.detailData = {};
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