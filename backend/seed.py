import requests
import random

BASE_URL = 'http://localhost:5000'  # Replace with your Flask app's URL

NAMES_LIST = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Krishna", "Sai", "Aryan", "Dhruv", 
    "Karthik", "Shreyas", "Nikhil", "Rohan", "Siddharth", "Yash", "Rudra", "Ishaan", 
    "Om", "Arjun", "Ananya", "Aditi", "Meera", "Pooja", "Priya", "Sana", "Riya"
]

SONG_TITLES = [
    "Shape of You", "Blinding Lights", "Perfect", "Happier", "Stay", 
    "Levitating", "Senorita", "Believer", "Lovely", "Despacito"
]

PLAYLIST_NAMES = [
    "Chill Vibes", "Workout Tunes", "Road Trip Jams", "Evening Relaxation", 
    "Party Hits", "Morning Motivation", "Top Hits", "Soft Melodies"
]

def get_random_name():
    return random.choice(NAMES_LIST)

def get_random_song_title():
    return random.choice(SONG_TITLES)

def get_random_playlist_name():
    return random.choice(PLAYLIST_NAMES)

def register_user(username, email, password):
    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "email": email,
        "password": password,
        "role" : 'creator',
    })
    return response.json()

def login_user(email, password):
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    return response.json()

def create_song(auth_token, title, artist, creator_id):
    headers = {'Authentication-Token': auth_token}
    response = requests.post(f"{BASE_URL}/api/songs", json={
        "title": title,
        "artist": artist,
        "creator_id" : creator_id,
    }, headers=headers)
    return response.json()

def create_playlist(auth_token, name):
    headers = {'Authentication-Token': auth_token}
    response = requests.post(f"{BASE_URL}/api/playlists", json={"name": name}, headers=headers)
    return response.json()

def add_song_to_playlist(auth_token, playlist_id, song_id):
    headers = {'Authentication-Token': auth_token}
    response = requests.post(f"{BASE_URL}/api/playlists/{playlist_id}/songs", json={
        "song_id": song_id
    }, headers=headers)
    return response.json()

def seed_database():
    users = []
    
    # Register and login users
    for i in range(10):
        username = get_random_name()
        email = f"{username.lower()}@example.com"
        password = "1234"
        register_user(username, email, password)
        login_response = login_user(email, password)
        if 'token' in login_response:
            users.append({"username": username, "email": email, "token": login_response['token'], 'creator_id' : login_response['creator_id'], 'user_id' : login_response['id']})
    
    # Create songs and playlists for each user
    for user in users:
        auth_token = user['token']
        creator_id = user['creator_id']
        user_id = user['user_id']
        song_ids = []
        
        # Create 5 songs per user
        for _ in range(5):
            title = get_random_song_title()
            artist = f"{get_random_name()} Band"
            song = create_song(auth_token, title, artist, creator_id = creator_id)
            if 'id' in song:
                song_ids.append(song['id'])
        
        # Create 2 playlists per user
        for _ in range(2):
            playlist_name = get_random_playlist_name()
            playlist = create_playlist(auth_token, playlist_name)
            if 'id' in playlist:
                playlist_id = playlist['id']
                
                # Add 3 random songs to each playlist
                for song_id in random.sample(song_ids, k=3):
                    add_song_to_playlist(auth_token, playlist_id, song_id)

if __name__ == "__main__":
    seed_database()
