from flask import Flask, redirect, request, jsonify, render_template, session, url_for
import os
from dotenv import load_dotenv
from spotify_client import (
    get_auth_url, handle_callback, get_spotify_client,
    get_current_user, get_user_playlists, get_playlist_data, logout
)
from genai_client import get_roast

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "sjdjsdjhdsfdiddhkjsdkjsdjforferuavsjfvnvbkfashwoelh348981-34tue2iit';lkwdbfkvjefmbodfjfv,nsddbfflnvsdnfnvl;wfnvkd")


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    sp = get_spotify_client()
    logged_in = sp is not None
    user = get_current_user(sp) if logged_in else None
    return render_template("index.html", logged_in=logged_in, user=user)


@app.route("/login")
def login():
    auth_url = get_auth_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")

    if error or not code:
        return redirect(url_for("index") + "?auth_error=1")

    success = handle_callback(code)
    if not success:
        return redirect(url_for("index") + "?auth_error=1")

    return redirect(url_for("index"))


@app.route("/logout")
def logout_route():
    logout()
    return redirect(url_for("index"))


@app.route("/api/playlists")
def api_playlists():
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "not_authenticated"}), 401

    playlists = get_user_playlists(sp)
    return jsonify({"playlists": playlists})


@app.route("/api/roast", methods=["POST"])
def api_roast():
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "not_authenticated"}), 401

    data = request.get_json()
    playlist_id = data.get("playlist_id")
    playlist_name = data.get("playlist_name", "your playlist")
    cover_url = data.get("cover_url", None)

    if not playlist_id:
        return jsonify({"error": "missing playlist_id"}), 400

    tracks = get_playlist_data(sp, playlist_id)

    print("[DEBUG] playlist_id:", playlist_id)
    print("[DEBUG] tracks count:", len(tracks) if tracks else 0)
    print("[DEBUG] sample:", tracks[:2] if tracks else "EMPTY")

    if not tracks:
        return jsonify({"error": "empty_playlist"}), 422

    roast = get_roast(tracks)

    return jsonify({
        "roast": roast,
        "playlist_name": playlist_name,
        "cover_url": cover_url,
        "track_count": len(tracks)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

