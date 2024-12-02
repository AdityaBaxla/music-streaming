<template>
    <div class="container mt-5">
      <div class="card p-4">
        <h3 class="text-center">Login</h3>
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
          <button class="btn btn-primary w-100" @click.prevent="sendLogin">
            Login
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

