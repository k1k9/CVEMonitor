<template>
    <footer>
        <p>© {{ new Date().getFullYear() }} CVE Monitor</p>
        <p>This product uses the NVD API but is not endorsed or certified by the NVD.</p>
    </footer>
</template>

<style scoped lang="scss">
footer{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 1rem;
    box-sizing: border-box;
    padding: 1rem;
    opacity: 0.5;

    &:hover{
        opacity: 1;
        cursor: default;
    }

    @media (min-width: 768px){
        flex-direction: row;
        padding: 2rem 0 4rem 0;
    }

    p{
        margin: 0;
        padding: 0;
    }
}
</style>