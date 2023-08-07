import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests

load_dotenv()

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
song_titles =  soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_titles]
print(song_names)


# sp = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         scope="playlist-modify-private",
#         redirect_uri="http://example.com",
#         client_id=os.getenv("CLIENT_ID"),
#         client_secret=os.getenv("CLIENT_SECRET"),
#         show_dialog=True,
#         cache_path="token.txt",
#         username="Majedul Islam", 
#     )
# )
# user_id = sp.current_user()["id"]
