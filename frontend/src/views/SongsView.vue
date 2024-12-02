<template>
  <button @click="$router.push('/songs/upload')">Upload</button>
  <div>Your Songs:</div>
  <div class="container">
    <div class="row">
      <div class="col-md-4 col-sm-6 col-12 card-container mb-2" v-for="song in songs" :key="song.id">
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
import SongComponent from "@/components/SongComponent.vue";
import { customFetch } from "@/utils/customFetch";

export default {
  data() {
    return {
      songs: [],
    };
  },
  methods: {
    async getSongs() {
      const res = await customFetch("/api/songs");
      this.songs = await res.json();
      console.log(this.songs)
    },
  },
  mounted() {
    this.getSongs();
  },
  components: {
    SongComponent,
  },
};
</script>

<style scoped>
.song-comp {
  margin: 2em;
}

.card-container {
    margin: 1rem; /* Adjust the margin as needed */
}
</style>
