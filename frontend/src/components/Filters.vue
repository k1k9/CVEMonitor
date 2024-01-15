<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useToast } from "vue-toastification";

const toast = useToast();
const store = useStore();
const filters = ref([]);
const props = defineProps({
  offset: {
    type: Number,
    default: 15,
  },
  headless: {
    type: Boolean,
    default: false,
  }
});

function loadFilters() {
    axios.get('/filters')
        .then(response => {
            filters.value = response.data.map(filter => filter.id);
        })
        .catch((error) => {
            if (error.response.status === 401) {
                store.dispatch("logout");
                toast.error("Session expired");
            } else {
                toast.error("Error loading alerts");
            }
        });
}

function removeFilter(filterName) {
    axios.delete(`/filter/${filterName}`)
        .then(response => {
            loadFilters();
            toast.success(`Filter ${filterName} deleted`);
        })
        .catch(error => {
            toast.error("Error deleting filter");
        });
}

onMounted(loadFilters);
</script>

<template>
    <section class="filters">
        <h2 v-if="!headless">Filters</h2>
        <ul v-if="offset !== 0">
            <li v-for="filter in filters.slice(0, offset)" :key="filter">
                {{ filter }}
            </li>
            <li v-if="filters.length > offset" class="showAll">
                <RouterLink to="/filters">Show all</RouterLink>
            </li>
        </ul>
        <ul v-if="offset === 0" class="more">
            <li v-for="filter in filters" :key="filter">
                {{ filter }}
                <button class="remove" @click="() => removeFilter(filter)">
                    X
                </button>
            </li>
        </ul>
    </section>
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";
.filters{
    width: 100%;
    ul{
        width: 100%;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        list-style: none;
        margin:0;
        padding: 0;
        box-sizing: border-box;
        gap: 1.5rem;
        flex-wrap: wrap;

        &.more{
            width: 100%;
            @media (min-width: 1000px) {
                justify-content: space-between;
                grid-template-columns: 1fr 1fr 1fr 1fr;
            }
        }

        li{
            padding: .5rem .75rem;
            border-radius: 5px;
            background-color: $lighter-background;
            text-align: center;

            display: flex;
            justify-content: space-between;
            align-items: center;

            .remove{
                background-color: transparent;
                color: $alert-high;
                border: none;
                border-radius: 5px;
                padding: .5rem .75rem;
                font-size: 1rem;
                cursor: pointer;
            }
            
            &.showAll{
                background-color: transparent;
                padding:0;
                
                a{ 
                    padding: .5rem .75rem;
                    border-radius: 5px;
                    width: 100%;
                    background-color: none;
                    color: $white;
                    text-decoration: none;

                    &:hover{
                        opacity: 0.7;
                    }
                }
            }
        }
    }
}
</style>