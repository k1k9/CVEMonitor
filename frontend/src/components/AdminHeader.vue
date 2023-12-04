<script setup>
</script>



<template>
    <ul>
        <li>
            <RouterLink to="/users">Users</RouterLink>
        </li>

        <li>
            <RouterLink to="/users">Management</RouterLink>
        </li>
    </ul>
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";

ul{
    width: 100%;
    height: auto;
    display: flex;
    align-items: center;
    list-style: none;
    margin: 0;
    padding:0;
    gap: 2rem;
    justify-content: center;

    @media(min-width: 768px){
        justify-content: flex-end;
    }

    li{
        a{
            color: $darker-foreground;
            text-decoration: none;
            font-size: 1rem;

            &:hover{
                opacity: 0.5;
            }
        }
    }
}
</style>