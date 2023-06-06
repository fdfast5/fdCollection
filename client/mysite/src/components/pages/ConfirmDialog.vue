<template>
    <v-row justify="center">
        <v-dialog
            v-model="confirmDialog"
            :persistent='true'
            width="40%"
            height="50%"
            no-click-animation
            >
            <v-card class="pa-3">
                <v-card-title class="card-title-frame">
                    <span class="card-title">更新確認</span>
                </v-card-title>
                    <v-card-text>
                        更新します。よろしいですか？
                    </v-card-text>
                    <v-btn
                        class="mb-4"
                        @click="update()"
                    >
                        更新
                    </v-btn>
                    <v-btn
                        @click="cancel()"
                    >
                        キャンセル
                    </v-btn>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>

export default {
    props: [
        'open'
    ],
    data () {
        return {
        };
    },
    computed: {
        confirmDialog: {
            get () {
                return this.open;
            }
        }
    },
    methods: {
        /** --------------
         * 更新
         * -------------*/
        update() {
            this.$emit('save');
        },
        /** ----------
         * キャンセル
         * -----------*/
        cancel() {
            this.$emit('cancel');
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