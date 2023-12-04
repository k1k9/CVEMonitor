<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import router from '../router';

const store = useStore();
const username = ref('');
const password = ref('');

function login() {
  store.dispatch('login', {
    username: username.value,
    password: password.value
  })
  .then(() => {
    router.push('/');
  })
  .catch(error => {
    console.error(error);
  });
}
</script>

<template>
    <section class="login">
      <form @submit.prevent="login">
        <h2>Login</h2>
            <input type="text" id="username" 
                    v-model="username" required
                    placeholder="Username"/>

            <input type="password" id="password"
                    v-model="password" required
                    placeholder="Password"/>

            <button type="submit">Login</button>
        </form>
    </section>
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";
section.login{
  width: 100%;
  min-height: 85vh;
  box-sizing: border-box;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;

  
  form{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 1rem 0;
    background-color: $lighter-background;
    margin: auto;
    padding: 2rem 3rem;
    border-radius: 5px;
    box-sizing: border-box;
    overflow: hidden;
    width: 96%;

    @media (min-width: 768px){
      width: 400px;
      gap: 2rem;
      padding: 3rem 5rem;
    }

    h2{
      text-align: center;
      padding-bottom: 1rem;
    }

    input{
      padding: .5rem;
      border-radius: 5px;
      border: 1px solid $foreground;
      background-color: $lighter-background;
      color: $foreground;
      font-size: 1rem;
      font-weight: 700;
      box-sizing: border-box;
      outline: none;

      &:focus{
        border: 1px solid $accent;
      }
    }

    button{
      padding: .5rem;
      border-radius: 5px;
      border: 1px solid $foreground;
      background-color: $lighter-background;
      color: $foreground;
      font-size: 1rem;
      font-weight: 700;
      box-sizing: border-box;
      outline: none;
      cursor: pointer;

      &:hover{
        background-color: $accent;
        color: white;
        border: 1px solid $accent;
      }
    }
  }
}
</style>