"""
description_utils.py

Utility functions for generating video descriptions dynamically using OpenAI's API.
Includes brand-aware humor, format-aware descriptions, and dynamic prompt generation.

This module currently supports:
- Montage descriptions (fun, quirky, "Cool-Hand Gramps" themed)

Author: Llama Chile Shop
Created: 2025-07-22
"""

import os
import random
import openai

# 🛠 Global debug flag (imported by design elsewhere)
from modules.config import DEBUG

# Set up OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_montage_description() -> str:
    """
    Generates a creative, humorous description for a montage highlight video.
    Leverages the "Cool-Hand Gramps" branding identity and inserts dynamic randomness
    to keep each description fresh and engaging.

    Returns:
        str: A YouTube/PeerTube-ready video description.
    """
    # 🎲 Add entropy to reduce prompt caching / same-seed behavior
    creativity_seed = random.randint(0, 999999)

    # 🧠 Base template for the prompt
    prompt = f"""
You are a branding-savvy copywriter helping a YouTube gaming channel called "Llama Chile Shop" 
run by a quirky and beloved senior gamer named "Gramps." Gramps is known for his calm demeanor, 
sharp shooting, and whacky senile playstyle in Solo Zero Build Fortnite matches. His fans refer 
to him as "Cool-Hand Gramps" because his heart rate doesn’t rise, even in intense firefights.

Write a YouTube/PeerTube video description for a highlight montage from one of Gramps' livestreams. 
Make it short, funny, and on-brand. Include emoticons and hashtags. Add a sentence encouraging viewers 
to subscribe and check out the stream calendar.

Entropy seed: {creativity_seed}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative and humorous copywriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        fallback = "Join Gramps for another action-packed Fortnite montage! Subscribe and watch live ➡ https://youtube.com/@llamachileshop 🎮🦙 #Fortnite #CoolHandGramps"
        if DEBUG:
            print(f"[ERROR] Failed to generate montage description: {e}")
        return fallback
