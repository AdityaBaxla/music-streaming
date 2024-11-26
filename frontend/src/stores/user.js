import { ref, computed } from 'vue'
import { defineStore, setActivePinia } from 'pinia'

export const useUserStore = defineStore('user', {
  state : () => {
    return {
      token : null,
      user_name : null,
      user_id : null,
      creator_id : null,
      email : null,
      role : null,
    }
  },
  getters: {
    isAuthenticated(state) {
      return !!state.token;
    },
    userName(state) {
      return state.user_name ? state.user.name : 'Guest';
    },
  },
  actions: {
    setUser(user) {
      if (!!user){
        console.log('user exists')
        localStorage.setItem('user', JSON.stringify(user))
      }

      try{
       if (JSON.parse(localStorage.getItem('user'))){
         const user = JSON.parse(localStorage.getItem('user'));
         console.log('inside if ')
          this.token = user.token;
          this.role = user.role;
          this.user_id = user.id;
          this.email = user.email;
          this.creator_id = user.creator_id;
       }
      } catch {
          console.warn('not logged in')
  }         
  },
    logout() {
      this.token = null
      this.user_name = null
      this.user_id = null
      this.creator_id = null
      this.email = null
      this.role = null
    },
  },
  // persist : true, // enable persistence
}
)
