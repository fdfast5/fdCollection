<template>
    <v-container>
        <v-btn class="pink white--text" @click="twitchLogin">Twitch Login</v-btn>
    </v-container>
</template>

<script>
// import router from "../../router";
export default {
    name: "fd-collection-login",
    mounted() {
        if (location.hash) {
            console.log(location.hash);
        }
    },
    methods: {
        twitchLogin() {
            let client_id = 'kfka7cipofpyncxov9lrhu0l6qnmjx'; // envで持つ想定
            let redirect_uri = 'http://localhost:8080/#/login'; // envで持つ想定
            window.location.href = 'https://id.twitch.tv/oauth2/authorize?client_id=' + client_id + '&redirect_uri=' + encodeURIComponent(redirect_uri) + '&response_type=token'
        }
    }
};
</script>