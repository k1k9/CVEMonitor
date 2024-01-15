<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  stats: {
    type: Array,
    default: () => [],
    validator: (value) => {
      return value.every(subArray => 
        Array.isArray(subArray) && 
        subArray.length === 2 && 
        typeof subArray[0] === 'string' && 
        typeof subArray[1] === 'number'
      );
    }
  }
});
</script>


<template>
  <section class="stats">
    <h2>Stats</h2>
    <ul>
      <li v-for="(item, index) in stats" :key="index">
        <span class="number">{{ item[1] }}</span>
        <p>{{ item[0] }}</p>
      </li>
    </ul>
  </section>
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";

section.stats{
    width: 100%;

    @media (min-width: 900px) and (max-width: 1000px){
            h2{
              display: none;
            }
        }

    ul{
        width: 100%;
        background: $lighter-background;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        align-items: center;
        list-style: none;
        margin: 0;
        gap: 3rem;
        box-sizing: border-box;
        padding: 1rem;
        border-radius: 5px;

        @media (min-width: 900px) and (max-width: 1000px){
            grid-template-columns: repeat(6,1fr);
            padding: .5rem;
        }

        li{
            text-align: center;

            .number{
                font-size: 2rem;
                @media (min-width: 900px) and (max-width: 1000px){
                    font-size: 1.2rem;
                }
            }

            p{
                padding: 1rem 0 0 0;
                margin:0;
                @media (min-width: 900px) and (max-width: 1000px){
                  padding: .5rem 0 0 0;
                }
            }
        }
    }    
}
</style>