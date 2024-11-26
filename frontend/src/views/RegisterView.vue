<template>
    <div>
        <input placeholder="email" v-model="email">
        <input placeholder="password" v-model="password">
        <input placeholder="username" v-model="username">
        <input type="checkbox" id="creator" v-model="isCreator" >
        <label for="creator">Creator</label>
        <input v-if="isCreator" placeholder="Artist Name" v-model="artist_name">
        <button class="btn btn-primary" @click="sendRegister">Signup</button>
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
            username : '',
            isCreator : false,
            artist_name : '',
        }
    },
    computed: {
        role() {
            return this.isCreator ? 'creator' : 'user' 
        }
    },
    methods : {
        async sendRegister(){
            const res = await customFetch('/register', {auth : false,method : 'POST', body : JSON.stringify({'email' : this.email, 'password' : this.password, 'role' : this.role, 'username' : this.username, 'artist_name'  : this.isCreator ? this.artist_name : ''})})

            if (res.ok){
                alert('successfully registered, redirecting to login')
                this.$router.push('/login')
            }           
        }
    },
    mounted(){
        this.userStore = useUserStore();
    }
}

</script>

