<template>
    <div>
        現在リリース準備中
        <div v-for="item in collectionList" :key="item.id">
            <div
                @click="selectCollection(item.id)"
            >第{{ item.id }}弾</div>
        </div>
    </div>
</template>

<script>
// import axios from 'axios';
// import router from "../../router";
export default {
    name: "fd-collection-list",
    data: () => ({
        collectionList: [
            {id: 1},
            {id: 2},
            {id: 3}
        ],
        params: {}
    }),
    methods: {
        /** ----------------------------
         * コレクション選択
         * 2023-05 第一弾実装
         * ----------------------------- */
        selectCollection(id) {
            console.log(id);
        }
    }
};
</script>