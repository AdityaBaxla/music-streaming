<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6">
        <div class="form-group">
          <label for="title">Song Title:</label>
          <input type="text" v-model="title" id="title" class="form-control" required />
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <input type="text" 
 v-model="description" id="description" class="form-control" required />
        </div>
        <div class="form-group">
          <label for="playlist_id">Playlist ID:</label>
          <input type="text" v-model="playlist_id" id="playlist_id" class="form-control" required />
        </div>
      </div>
      <div class="col-md-6">
        <div class="form-group">
          <label for="mp3_file">Upload MP3:</label>
          <input type="file" @change="onFileChange($event, 'mp3')" id="mp3_file" accept=".mp3" class="form-control-file" required />
        </div>
        <div class="form-group">
          <label for="image_file">Upload Image:</label>
          <input type="file" @change="onFileChange($event, 'image')" id="image_file" accept="image/*" class="form-control-file" required />
        </div>
        <button type="button" class="btn btn-primary" @click="uploadFiles">Upload</button>
      </div>
    </div>
  </div>
</template>
  
  <script>
import { useUserStore } from '@/stores/user';
import { customFetch } from '@/utils/customFetch';

  export default {
    data() {
      return {
        title: '',
        mp3File: null,
        imageFile: null,
        playlist_id : '',
        description : '',
      };
    },
    methods: {
      onFileChange(event, type) {
        const file = event.target.files[0];
        if (type === 'mp3') {
          this.mp3File = file;
        } else if (type === 'image') {
          this.imageFile = file;
        }
      },
      async uploadFiles() {
        if (!this.title || !this.mp3File || !this.imageFile) {
          alert('Please provide all required inputs.');
          return;
        }
  
        const formData = new FormData();
        formData.append('name', this.title);
        formData.append('mp3_file', this.mp3File);
        formData.append('image_file', this.imageFile);
        formData.append('description', this.description);
        if (this.playlist_id) formData.append('playlist_id', this.playlist_id);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/songs', {
              method: 'POST',
              headers : {
                  'Authentication-Token' : this.userStore.token,
              },
              body: formData,
            });
  
          if (response.ok) {
            const result = await response.json();
            alert(result.message);
          } else {
            const error = await response.json();
            alert(`Upload failed: ${error.message}`);
          }
        } catch (error) {
          console.error('Error uploading files:', error);
          alert('An error occurred while uploading files.');
        }
      },
    },
    mounted(){
        this.userStore = useUserStore()
    }
  };
  </script>
  