<template>
  <div class="card" style="width: 18rem">
    <img class="card-img-top" src="..." alt="Card image cap" />
    <div class="card-body">
      <h5 class="card-title">{{ name }}</h5>
      <p class="card-text">
        {{ description }}
      </p>
      <h5 class="card-text">{{ artist_name }}</h5>
      <a href="#" class="btn btn-secondary">Play</a>
    </div>
  </div>
</template>

<script>
export default {
  props: ["name", "description", "song_id", "artist_name", "creator_id"],
  data() {},
};
</script>
