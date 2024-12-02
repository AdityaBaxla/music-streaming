<template>
  <div class="card" style="width: 18rem">
    <img class="card-img-top" :src="image_url" alt="Card image cap" />
    <div class="card-body">
      <h5 class="card-title">{{ name }}</h5>
      <p class="card-text">
        {{ description }}
      </p>
      <h5 class="card-text">{{ artist_name }}</h5>
      <a href="#" @click="play_song" class="btn btn-secondary">Play</a>
    </div>
  </div>
</template>

<script>
export default {
  props: ["name", "description", "song_id", "artist_name", "creator_id", "image_url", "audio_url"],
  methods:{
    play_song(){
      window.open(this.audio_url)
    }
  }
  };
</script>
