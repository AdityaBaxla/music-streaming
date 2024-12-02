<template>
    <div class="container">
      <div class="row">
        <div class="col-md-4 col-sm-6 col-12 card-container my-2" v-for="song in songs" :key="song.id">
          <SongComponent
            :name="song.name"
            :artist_name="song.artist_name"
            :creator_id="song.creator_id"
            :description="song.description"
            :image_url="song.image_url"
            :audio_url="song.audio_url"
          />
        </div>
      </div>
    </div>
</template>
  
  <script>
  import SongComponent from '@/components/SongComponent.vue';
import { useUserStore } from '@/stores/user';
  import { customFetch } from '@/utils/customFetch';
  
  export default {
    data() {
      return {
        songs: [],
      };
    },
    methods: {
      async getCreatorSongs() {
        try {
          const userStore = useUserStore(); // Access the store instance
          const res = await customFetch(`/api/creators/${userStore.creator_id}`);
          if (res.ok) {
            const data = await res.json();
            this.songs = data.songs || [];
            console.log(this.songs)
          } else {
            console.error("Failed to fetch songs.");
          }
        } catch (error) {
          console.error("Error fetching songs:", error);
        }
      },
    },
    mounted() {
      this.getCreatorSongs();
    },
    components:{
        SongComponent,
    }
  };
  </script>
  