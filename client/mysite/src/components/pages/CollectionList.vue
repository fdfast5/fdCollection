<template>
    <div>
        Collection Page
    </div>
</template>

<script>
import router from "../../router";
export default {
    name: "fd-collection",
    mounted() {
        this.checkLoggedIn();
    },
    methods: {
        checkLoggedIn() {
            if (!sessionStorage.getItem('token')) {
                router.push("/auth");
            }
        }
    }
};
</script>