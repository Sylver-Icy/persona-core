import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


#creates an OpenAI client object used to call the API
client = OpenAI()


# the structure  the LLM  is supposed to fill with extracted info
MEMORY_SCHEMA = {
    "preferences": {
        "likes": [],
        "dislikes": []
    },
    "emotional_patterns": {
        "tone_tendencies": []
    },
    "facts": {
        "name": "",
        "attributes": []
    }
}

def extract_memory(messages: list[str]) -> dict:
    """
    Takes list of user messages (30 strings)
    Sends them to LLM
    Returns memory JSON dict
    """

    #tell the LLM exactly:
    #what we want
    #what structure to output
    prompt = f"""
    You are a memory extraction engine for an AI assistant.

    Analyze the following raw user messages and extract:
    - user preferences
    - emotional patterns
    - factual info worth remembering long-term

    Return output ONLY as a JSON object matching this structure:

    {json.dumps(MEMORY_SCHEMA, indent=2)}

    User Messages:
    {messages}
    """

    #send a single prompt to generate JSON output
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You extract structured memory from conversation and respond ONLY with JSON matching the schema."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    # ---- 5) Extract raw returned text ----
    raw_output = response.choices[0].message.content

    # ---- 6) Parse JSON safely ----
    try:
        memory_dict = json.loads(raw_output)
    except Exception:
        # If model outputs invalid JSON for some reason, fallback to empty schema
        memory_dict = MEMORY_SCHEMA.copy()

    return memory_dict