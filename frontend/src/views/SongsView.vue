<template>
  <div>
    <SongComponent
      class="song-comp"
      v-for="song in songs"
      :key="song.id"
      :name="song.name"
      :artist_name="song.artist_name"
      :creator_id="song.creator_id"
      :description="song.description"
    >
    </SongComponent>
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
</style>
