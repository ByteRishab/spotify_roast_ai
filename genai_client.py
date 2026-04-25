import os
from dotenv import load_dotenv

load_dotenv()

def get_roast(track_list: list[dict]) -> str:
    """
    Takes a list of { track_name, artist } dicts and returns a roast string.
    Falls back gracefully if the API fails.
    """
    try:
        from google import genai
        from google.genai import types

        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            return "The AI couldn't find its API key. Even your secrets are a mess, huh?"

        # Format tracklist for the prompt
        formatted = "\n".join(
            track_list
        )

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f'Take a look at this playlist:\n"""\n{formatted}\n"""\nI dare you to roast me.',
            config=types.GenerateContentConfig(
                system_instruction="""
You are a savage but loveable best friend who roasts playlists.
Rules:
- Reference specific artists or song titles from the list
- Call out patterns you notice (e.g. too many breakup songs, one-genre tunnel vision)
- Be witty, use pop culture references
- End with ONE backhanded compliment
- Max 150 words — punchy, not an essay
- Never be cruel or personal — it's all in good fun
"""
            )
        )
        print(f"[genai_client] API response: {response.text}")
        return response.text

    except Exception as e:
        print(f"[genai_client] get_roast error: {e}")
        return "The AI took one look at your playlist and had to lie down. Try again when it recovers."

