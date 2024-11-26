<template>
    <div>
        <div v-for="song in songs">
            <h2>{{ song.name }}</h2>
            <h3>{{ song.description }}</h3>
            <h3>{{ song.creator.artist_name }}</h3>
        </div>
    </div>
</template>

<script>
import { customFetch } from '@/utils/customFetch';

    export default {
        data(){
            return {
                songs : []                
            }
        },
        methods : {
            async getSongs(){
                const res = await customFetch('/api/songs')
                this.songs = await res.json()
            }
        },
        mounted(){
             this.getSongs()
        },
    }
</script>
