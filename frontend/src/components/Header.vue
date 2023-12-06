<script setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import router from '../router';
import { RouterLink } from 'vue-router';
import AdminHeader from './AdminHeader.vue';
import { useToast } from "vue-toastification";

const toast = useToast();
const store = useStore();
const isAuthenticated = computed(() => store.getters.isAuthenticated);
const isAdmin = computed(() => store.getters.isAdmin);
const showMobileMenu = ref(false);

function logout() {
    store.dispatch('logout')
    .then(() => {
        router.push('/');
        toast.info("Logged out");
    })
    .catch(error => {
        console.error(error);
    });
}
</script>


<template>
    <header class="mainHeader">
        <h1>
            <RouterLink to="/">CVE Monitor</RouterLink>
        </h1>

        <ul class="desktop">
            <li>
                <RouterLink to="/">Home</RouterLink>
            </li>
            <li v-if="isAuthenticated">
                <RouterLink to="/filters">Filters</RouterLink>
            </li>
            <li v-if="!isAuthenticated">
                <RouterLink to="/login">Login</RouterLink>
            </li>
            <li v-if="isAuthenticated">
                <p @click="logout">Logout</p>
            </li>
        </ul>

        <!-- Mobile -->
        <button @click="showMobileMenu = !showMobileMenu">
            <span v-if="!showMobileMenu">MENU</span>
            <span v-if="showMobileMenu">X</span>
        </button>

        <ul class="mobile" v-if="showMobileMenu">
            <li>
                <RouterLink to="/">Home</RouterLink>
            </li>
            <li>
                <RouterLink to="/filters">Filters</RouterLink>
            </li>

            <li v-if="!isAuthenticated">
                <RouterLink to="/login">Login</RouterLink>
            </li>
            <li v-if="isAuthenticated">
                <p @click="logout">Logout</p>
            </li>
        </ul>
    </header>

    <AdminHeader v-if="isAdmin" />
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";

header{
    display: flex;
    position: relative;
    justify-content: center;
    padding: 1rem 0;
    box-sizing: border-box;

    @media (min-width: 768px){
        justify-content: space-between;
        align-items: center;
    }

    h1{
        margin: 0;
        padding: 0;
        font-size: 2rem;
        font-weight: 500;
        
        a{
            color: $foreground;
            text-decoration: none;
        }
    }

    ul.desktop{
        display: none;

        @media (min-width: 768px){
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 0;
            list-style: none;
            gap: 2rem;

            li{
                a,p{
                    color: $foreground;
                    padding: 1rem 0;
                    font-size: 1.3rem;
                    text-decoration: none;
                    &:hover{
                        cursor: pointer;
                        opacity: 0.7;
                    }
                }
            }
        }
    }

    button{
        display: block;
        background: none;
        border: none;
        color: $foreground;
        padding: 1rem;
        margin: 0;
        position: absolute;
        top:1vh;
        right: 1vw;
        z-index: 999;
        @media (min-width: 768px){ display: none}

        &:hover{
            cursor: pointer;
            opacity: 0.7;
        }
    }

    ul.mobile{
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: absolute;
        top:0;
        left:0;
        width: 100%;
        height: 100vh;
        margin: 0;
        background-color: $lighter-background;
        box-sizing: border-box;
        overflow: hidden;
        list-style: none;
        gap: 2rem;
        z-index: 998;

        @media (min-width: 768px){ display: none}

        li{
            a{
                color: $foreground;
                padding: 1rem 0;
                font-size: 1.3rem;
                text-decoration: none;
                &:hover{
                    cursor: pointer;
                    opacity: 0.7;
                }
            }
        }
    }
}
</style>