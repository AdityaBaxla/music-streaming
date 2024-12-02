
<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand" >Songify</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="artists" class="nav-link">Artists</router-link>
            </li>
            <li class="nav-item">
              <router-link to="profile" class="nav-link">Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="userStore.role == 'admin' ? '/admin-dashboard' : '/creator-dashboard' " class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link to="songs" class="nav-link">Songs</router-link>
            </li>
            <button class="btn btn-primary" @click="logout">
            Logout
          </button>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  <script>
  import { useUserStore } from '@/stores/user';
  import { mapStores } from 'pinia';
  
    export default {
        computed : {
            ...mapStores(useUserStore)
        },
        methods : {
            logout(){
                this.userStore.logout()
                this.$router.push('/')
            }
        }
    }
</script>