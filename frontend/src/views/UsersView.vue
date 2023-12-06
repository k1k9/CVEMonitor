<script setup>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import { useToast } from "vue-toastification";

const store = useStore();
const users = ref([]);
const isAdmin = computed(() => store.getters.isAdmin);

// Register user
const registerButton = ref(false);
const username = ref('');
const password = ref('');
const permissions = ref('');
const toast = useToast();


function formatDate(date) {
  const inputDate = new Date(date);
  const day = inputDate.getDate().toString().padStart(2, "0");
  const month = (inputDate.getMonth() + 1).toString().padStart(2, "0");
  const year = inputDate.getFullYear().toString().slice(-2);
  const hours = inputDate.getHours().toString().padStart(2, "0");
  const minutes = inputDate.getMinutes().toString().padStart(2, "0");
  const formattedDate = `${day}.${month}.${year} ${hours}:${minutes}`;
  return formattedDate;
}


function loadUsers() {
    axios.get('/users')
    .then(res => {
        users.value = res.data.map(user => ({ 
            ...user,
            created_at: formatDate(user.created_at),
            last_login: formatDate(user.last_login)
        }));
    })
    .catch(error => {
        toast.error("Error loading users");
    });
}

function deleteUser(userId) {
    axios.delete(`/user/${userId}`)
    .then((r) => {
        loadUsers();
        toast.success(`User ${userId} deleted`);
    })
    .catch(error => {
        toast.error("Error deleting user");
    });
}

function createUser() {
    axios.post('/user', {
        username: username.value,
        password: password.value,
        permissions: permissions.value
    })
    .then(() => {
        loadUsers();
        registerButton.value = false;
        toast.success(`User ${username.value} created`);
    });
}

onMounted(() => {
    loadUsers();
});
</script>

<template>
    <article v-if="registerButton" class="register">
        <header>
            <h2>Register</h2>
            <button @click="registerButton = !registerButton">X</button>
        </header>
        <form @submit.prevent="createUser">
            <input type="text" placeholder="Username" v-model="username" />
            <input type="password" placeholder="Password" v-model="password" />
            <input type="text" placeholder="Permissions" v-model="permissions" />
            <button type="submit">Register</button>
        </form>
    </article>


    <section class="users">
        <header>
            <h2>Users</h2>
            <span class="options">
                <button @click="loadUsers">Refresh</button>
                <button @click="registerButton = !registerButton">Register</button>
            </span>
        </header>
        <ul>
            <li>
                <span class="info">
                    <p>Username</p>
                    <p>Perms</p>
                    <p>Created</p>
                    <p>Last login</p>
                </span>

            </li>

            <li v-for="user in users" :key="user.id">
                <span class="info">
                    <p>{{ user.username }}</p>
                    <p>{{ user.permissions }}</p>
                    <p>{{ user.created_at }}</p>
                    <p>{{ user.last_login }}</p>
                </span>

                <span class="actions">
                    <button class="delete" @click="() => deleteUser(user.id)">Delete</button>
                </span>
            </li>
        </ul>
    </section>
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";

.register{
    position: absolute;
    top: 50%;
    left:50%;
    transform: translate(-50%, -50%);
    width: 90%;
    background:$table-header;
    z-index: 1000;
    box-sizing: border-box;
    overflow: hidden;
    padding: 2rem;
    border-radius: 5px;
    border: 1px solid $darker-foreground;

    @media (min-width: 768px){
        width: 70%;
    }

    @media (min-width: 1200px){
        width: 50%;
    }

    header{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 4rem;
        h2{
            padding:0;
        }
    }

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
            border: none;
            outline: none;
            box-sizing: border-box;
            background: none;
            color: $darker-foreground;
            border: 1px solid $darker-foreground;
        }

        button{
            padding: .5rem;
            background: none;
            border: 1px solid $darker-foreground;
            border-radius: 5px;
            color: $darker-foreground;
        }
    
    }
}

.users{
    width: 100%;
    min-height: 79vh;
    box-sizing: border-box;
    padding-top: 3rem;
    box-sizing: border-box;


    @media (min-width: 768px){
        width: 80vw;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        // justify-content: center;
        align-items: center;
    }

    @media (min-width: 1200px){
        width: 70vw;
    }

    header{
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;

        h2{
            margin:0;
            padding:0;
        }

        .options{
            display: flex;
            gap: 1rem;

            button{
            padding: .5rem;
            background: none;
            border: 1px solid $darker-foreground;
            border-radius: 5px;
            color: $darker-foreground;
        }
        }
    }

    ul{
        width: 100%;
        box-sizing: border-box;
        overflow: hidden;
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 2rem;
        margin:0;
        padding:0;
        
        li{
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 1rem;
            border-radius: 5px;
            box-sizing: border-box;


            &:nth-child(odd){
                background: $table-odd-child;
            }

            &:first-child{
                border-bottom: none;
                background: $table-header;
                color: $table-header-fg;
                padding-top: 1rem;
                border-radius: 5px;
            }

            .info{
                display: grid;
                grid-template-columns: 1fr .5fr 1.25fr 1.25fr;
                gap: 1rem;
                margin:0;
                padding:0;
                align-items: center;
                width: 90%;
                

                p{
                    width: 100%;
                    margin:0;
                    padding:0;
                    border-left: 1px solid $darker-foreground;
                    padding-left: 1rem;
                    justify-self: center;

                    &:first-of-type{
                        border-left: none;
                    }
                }
            }

            .actions{
                width: 10%;
                display: none;

                @media (min-width: 768px){
                    display: flex;
                    justify-content: flex-end;
                    align-items: center;
                    gap: 1rem;
                }

                .delete{
                    padding: .2rem;
                    background: none;
                    color: $red;
                }
            }
        }
    }
}
</style>