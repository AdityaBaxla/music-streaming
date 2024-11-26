<template>
    <div>
        <input placeholder="email" v-model="email">
        <input placeholder="password" v-model="password">
        <button class="btn btn-primary" @click="sendLogin">Login</button>
    </div>
</template>


<script>
import { customFetch } from '@/utils/customFetch';
import { useUserStore } from '@/stores/user';

export default { 
    data(){
        return {
            email : '',
            password : '',
        }
    },
    methods : {
        async sendLogin(){
            const res = await customFetch('/login', {auth : false,method : 'POST', body : JSON.stringify({'email' : this.email, 'password' : this.password})})

            if (res.ok){
                const userData = await res.json()
                this.userStore.setUser(userData)
                this.$router.push('/songs')
            }           
        }
    },
    mounted(){
        this.userStore = useUserStore();
    }
}

</script>

