<template>
    <div class="container mt-5">
      <div class="card p-4">
        <h3 class="text-center">Signup</h3>
        <form>
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
              type="email"
              id="email"
              class="form-control"
              placeholder="Enter your email"
              v-model="email"
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              id="password"
              class="form-control"
              placeholder="Enter your password"
              v-model="password"
            />
          </div>
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              id="username"
              class="form-control"
              placeholder="Enter your username"
              v-model="username"
            />
          </div>
          <div class="form-check mb-3">
            <input
              class="form-check-input"
              type="checkbox"
              id="creator"
              v-model="isCreator"
            />
            <label class="form-check-label" for="creator">Are you a creator?</label>
          </div>
          <div class="mb-3" v-if="isCreator">
            <label for="artist_name" class="form-label">Artist Name</label>
            <input
              type="text"
              id="artist_name"
              class="form-control"
              placeholder="Enter your artist name"
              v-model="artist_name"
            />
          </div>
          <button class="btn btn-primary w-100" @click.prevent="sendRegister">
            Signup
          </button>
        </form>
      </div>
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

