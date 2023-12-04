<script setup>
import {ref} from 'vue'
import axios from 'axios'
import Filters from '../components/Filters.vue';
import router from '../router';
import { useStore } from 'vuex';

const store = useStore();

const newFilter = ref('');

function submitFilters(){
    axios.post('/filter', {
        id: newFilter.value.toLowerCase()
    })
    .then(() => {
        // refresh page
        router.go('/');
    });
}
</script>

<template>
    <section class="filtersView">
        <h2>Filters</h2>
        <form @submit.prevent="submitFilters">
            <input type="text" placeholder="Entry filter name" v-model="newFilter" />
            <button type="submit">Add</button>
        </form>

        <Filters :offset="0" :headless="true"/>
    </section>
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";
.filtersView{
    width: 100%;
    min-height: 79vh;
    box-sizing: border-box;
    padding-top: 3rem;

    @media (min-width: 768px){
        width: 60vw;
        margin: 0 auto;
    }

    @media (min-width: 1200px){
        width: 50vw;
    }

    h2{
        text-align: center;
    }

    form{
        width: 100%;
        display: grid;
        grid-template-columns: 1fr .5fr;
        justify-content: center;
        align-items: center;
        background-color: $lighter-background;
        font-size: 1.3rem;
        border-radius: 5px;

        @media (min-width: 768px){
            grid-template-columns: 1fr .3fr;
        }

        @media (min-width: 1200px){
            grid-template-columns: 1fr .1fr;
        }

        input[type=text]{
            background: none;
            border:none;
            color: $darker-foreground;
            outline: none;
            box-sizing: border-box;
            padding: .5rem;

            @media (min-width: 768px){
                padding: 1rem;
            }
        }

        button{
            background-color: $lighter-background;
            border: none;
            color: $darker-foreground;
            cursor: pointer;
            justify-self: stretch;
            text-align: right;
            border-left: 1px solid $darker-foreground;
            border-radius: 0;
            &:hover{
                color: $white;
                opacity: 1;
            }
        }
    }

    .filters{
        margin-top: 5rem;
    }
}
</style>