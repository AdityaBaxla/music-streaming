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

ARTIST_NAMES = [
    "Taylor Swift",
    "Adele",
    "Beyoncé",
    "Rihanna",
    "Ed Sheeran",
    "Justin Bieber",
    "Dua Lipa",
    "Harry Styles",
    "Lady Gaga",
    "The Weeknd",
    "Bruno Mars",
    "Katy Perry",
    "Ariana Grande",
    "Drake",
    "Maroon 5",
    "Eminem",
    "Billie Eilish",
    "Post Malone",
    "BTS",
    "BLACKPINK",
    "Michael Jackson",
    "Whitney Houston",
    "Elvis Presley",
    "Freddie Mercury",
    "Elton John",
    "Madonna",
    "Prince",
    "David Bowie",
    "Stevie Wonder",
    "Bob Dylan",
    "The Beatles",
    "Queen",
    "Led Zeppelin",
    "Pink Floyd",
    "The Rolling Stones",
    "AC/DC",
    "Nirvana",
    "Metallica",
    "Red Hot Chili Peppers",
    "Radiohead",
    "Jay-Z",
    "Kanye West",
    "Eminem",
    "Kendrick Lamar",
    "Drake",
    "The Beatles",
    "Queen",
    "Michael Jackson"
]

AUDIO_FILE = open('audio.mp3', 'rb')
IMAGE_FILE = open('image.png', 'rb')

def get_random_name():
    return random.choice(NAMES_LIST)

def get_random_song_title():
    return random.choice(SONG_TITLES)

def get_random_playlist_name():
    return random.choice(PLAYLIST_NAMES)

def get_random_artist():
    return random.choice(ARTIST_NAMES)

def register_user(username, email, artist_name, password):
    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "email": email,
        "password": password,
        "role" : 'creator',
        "artist_name" : artist_name,
    })
    return response.json()

def login_user(email, password):
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    return response.json()

def create_song(auth_token, title, artist, creator_id, description):
    headers = {'Authentication-Token': auth_token}
    files= {"mp3_file" : open('audio.mp3', 'rb'),
        "image_file" : open('image.png', 'rb'),}
    response = requests.post(f"{BASE_URL}/api/songs", data={
        "name": title,
        "artist": artist,
        "creator_id" : creator_id,
        "description" : description,
    }, headers=headers, files=files)
    return response.json()

def create_playlist(auth_token, name):
    headers = {'Authentication-Token': auth_token}
    response = requests.post(f"{BASE_URL}/api/playlists", json={"name": name}, headers=headers)
    return response.json()

def add_song_to_playlist(auth_token, playlist_id, song_id):
    headers = {'Authentication-Token': auth_token}
    response = requests.put(f"{BASE_URL}/api/songs/{song_id}", json={
        "song_id": song_id
    }, headers=headers)
    return response.json()

def seed_database():
    users = []
    
    # Register and login users
    for i in range(10):
        username = get_random_name()
        artist_name = get_random_artist()
        email = f"{artist_name.replace(' ', '').lower()}@abc.com"
        password = "pass"
        register_user(username, email, password=password, artist_name=artist_name)
        login_response = login_user(email, password)
        if 'token' in login_response:
            users.append({"username": username, "email": email, "token": login_response['token'], 'creator_id' : login_response['creator_id'], 'user_id' : login_response['id']})
    
    # Create songs and playlists for each user
    for user in users:
        auth_token = user['token']
        creator_id = user['creator_id']
        user_id = user['user_id']
        song_ids = []
        
        user['songs'] = []
        # Create 5 songs per user
        for _ in range(5):
            title = get_random_song_title()
            artist = f"{get_random_name()} Band"
            song = create_song(auth_token, title, artist, creator_id = creator_id, description='lorem ipsum')
            if 'id' in song:
                user['songs'].append(song['id'])
        print(user['songs'])
        
        # Create 2 playlists per user
        for _ in range(2):
            playlist_name = get_random_playlist_name()
            playlist = create_playlist(auth_token, playlist_name)
            if 'id' in playlist:
                playlist_id = playlist['id']
                
                # Add 3 random ['songs'] to each playlist
                for song_id in random.sample(user['songs'], k=3):
                    add_song_to_playlist(auth_token, playlist_id, song_id)

if __name__ == "__main__":
    seed_database()
