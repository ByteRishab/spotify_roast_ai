import os
import spotipy
from flask import session
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

load_dotenv()

SCOPE = "playlist-read-private playlist-read-collaborative"

def get_auth_manager():
    cache_handler = FlaskSessionCacheHandler(session)

    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=SCOPE,
        cache_handler=cache_handler,
        show_dialog=True
    )

def get_spotify_client():
    """Returns an authenticated Spotipy client, or None if not authenticated."""
    try:
        auth_manager = get_auth_manager()
        token_info = auth_manager.get_cached_token()
        if not token_info:
            return None
        if auth_manager.is_token_expired(token_info):
            token_info = auth_manager.refresh_access_token(token_info['refresh_token'])
        return spotipy.Spotify(auth=token_info['access_token'])
    except Exception:
        return None

def get_auth_url():
    """Returns the Spotify OAuth authorization URL."""
    auth_manager = get_auth_manager()
    return auth_manager.get_authorize_url()

def handle_callback(code):
    """Exchanges auth code for token. Returns True on success."""
    try:
        auth_manager = get_auth_manager()
        auth_manager.get_access_token(code, as_dict=False)
        return True
    except Exception as e:
        print(f"[spotify_client] Callback error: {e}")
        return False

def get_current_user(sp):
    """Returns display name and user id, or None on failure."""
    try:
        user = sp.current_user()
        return {"display_name": user.get("display_name", "Friend"), "id": user.get("id")}
    except Exception as e:
        print(f"[spotify_client] get_current_user error: {e}")
        return None

def get_user_playlists(sp):
    """
    Returns a list of playlist dicts:
    { name, id, url, image_url, track_count }
    """
    try:
        results = sp.current_user_playlists(limit=50)
        playlists = []
        for p in results.get("items", []):
            if not p:
                continue
            images = p.get("images") or []
            image_url = images[0]["url"] if images else None
            playlists.append({
                "name": p.get("name", "Untitled"),
                "id": p.get("id"),
                "url": p.get("external_urls", {}).get("spotify", "#"),
                "image_url": image_url,
                "track_count": p.get("tracks", {}).get("total",0),
            })
        # print(playlists)
        return playlists

    except Exception as e:
        print(f"[spotify_client] get_user_playlists error: {e}")
        return []

def get_playlist_data(sp, pl_id):
    """
    Returns list of { track_name, artist } dicts for a given playlist id.
    Handles pagination and missing tracks safely.
    """
    try:
        # results = sp.playlist_tracks(playlist_id=pl_id, limit=100)
        # while results:
        songs = []
        print(pl_id)
        
        playlist_items = sp.playlist_tracks(playlist_id=pl_id, limit=100)
        # print(len(playlist_items['items']))
        track_durations_ms = []
        # print(track_durations_ms)
        
        for item in playlist_items['items']:
            song_name = item['item']['name']
            duration = item['item']['duration_ms']
            print(duration)
            track_durations_ms.append(duration)
            artist_names = 'By ' + ' and '.join([artist['name'] for artist in item['item']['artists']])
            track = song_name + ' ' + artist_names
            songs.append(track)
        #     for item in results.get("items", []):
        #         track = item.get("track")
        #         if not track:
        #             continue
        #         name = track.get("name")
        #         artists = track.get("artists", [])
        #         artist = artists[0]["name"] if artists else "Unknown"
        #         if name:
        #             tracks.append({"track_name": name, "artist": artist})
        #     results = sp.next(results) if results.get("next") else None
        return songs
    except Exception as e:
        print(f"[spotify_client] get_playlist_data error: {e}")
        return []

def logout():
    """Clears the cached Spotify token."""
    try:
        if os.path.exists(".spotify_cache"):
            os.remove(".spotify_cache")
    except Exception:
        pass


