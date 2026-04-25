--bg: #1a1a2e;           /* deep navy background */
--card: #16213e;         /* slightly lighter card bg */
--accent: #e94560;       /* hot pink/red — primary CTA */
--accent2: #0f3460;      /* deep blue — secondary */
--text: #eaeaea;         /* off-white text */
--muted: #a0a0b0;        /* muted secondary text */
--green: #1DB954;        /* Spotify green — use only for Spotify button */
```

**Typography:**
- Headings: `Fredoka One` (Google Fonts)
- Body: `Nunito` (Google Fonts)
- Load both in a single `<link>` tag

**Component Rules:**
- Border radius: always `16px` or `24px` — nothing sharp
- Buttons: pill-shaped (`border-radius: 999px`), bold text, subtle box-shadow, scale up 5% on press (`transform: scale(1.05)`)
- Cards: `border-radius: 20px`, faint border `1px solid rgba(255,255,255,0.08)`, hover lifts with shadow
- All tap targets minimum `48px` tall (mobile-friendly)
- No horizontal scrolling ever

**Micro-interactions (CSS only unless noted):**
- Playlist cards: `@keyframes wiggle` on `:hover/:active`
- Spotify login button: pulse glow animation
- Roast speech bubble: bounces in with `@keyframes bounceIn`
- Loading spinner: pure CSS spinning vinyl record (circle + center dot + grooves via `conic-gradient`)

---

## Flask Routes
```
GET  /                    → Serve the single HTML shell
GET  /login               → Redirect to Spotify OAuth
GET  /callback            → Handle OAuth callback, store token, redirect to /
GET  /api/playlists       → Return JSON list of user's playlists
POST /api/roast           → Body: {playlist_id}, returns {roast, playlist_name, cover_url}
GET  /logout              → Clear session, redirect to /
```

All `/api/` routes return JSON. Frontend uses `fetch()` to call them and updates the DOM in place.

---

## Error Handling (must feel friendly, not technical)

- Spotify auth failure → show: *"Spotify said no. Try again? 😬"*
- Empty playlist → *"Babe, the playlist is empty. What am I supposed to roast?"*
- GenAI timeout/error → *"The AI is too stunned to respond. Try again."*
- All errors appear as a dismissable toast notification (bottom of screen, slides up, auto-dismisses in 4s)

---

## Mobile UX Requirements

- Viewport meta tag: `width=device-width, initial-scale=1, maximum-scale=1`
- No horizontal scroll
- Playlist grid: 2 columns on mobile, 3 on tablet
- Touch-friendly — all interactions work with thumb tap
- Share button uses `navigator.share()` Web API (falls back to copy if unsupported)
- Safe area insets respected: `padding-bottom: env(safe-area-inset-bottom)`

---

## File Structure to Generate
```
/roast-my-playlist
  app.py                  ← Flask app + all routes
  spotify_client.py       ← Existing spotify functions (already written)
  genai_client.py         ← Existing get_roast() function (already written)
  templates/
    index.html            ← Entire frontend (HTML + CSS + JS in one file)
  .env                    ← SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SECRET_KEY
  requirements.txt        ← flask, spotipy, python-dotenv, (gemini/openai sdk)