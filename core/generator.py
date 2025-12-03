import json
from openai import OpenAI
from core.persona_engine import get_persona_prompt

client = OpenAI()


def generate_reply(user_message: str, persona: str, memory: dict):
    """
    Generates two replies:
    1) Base neutral reply using memory context
    2) Persona-stylized reply rewritten from the base
    """

    # build base response prompt
    base_prompt = f"""
You are an AI assistant with access to a persistent psychological profile of the user:

=== USER MEMORY ===
{json.dumps(memory, indent=2)}

Your job:
→ Produce a **neutral response** to the user's message.
→ The response MUST explicitly reflect relevant memory traits.
→ Avoid generic or universal advice — the answer should ONLY make sense for *this specific user*.

Rules:
1. Infer WHY the user behaves or asks this way by using memory.
2. Reference their preferences, frustrations, tone style, motivation triggers, learning style, etc.
3. Write in a neutral explanatory tone — no persona styling, slang, or theatrics.
4. Keep responses clear and concise, but personalized.

User message:
"{user_message}"

Write the response:
"""

    base_response = client.chat.completions.create(
        model="gpt-5-chat-latest",
        messages=[
            {"role": "system", "content": "You generate neutral responses using stored memory."},
            {"role": "user", "content": base_prompt}
        ],
        response_format={"type": "text"}
    ).choices[0].message.content

    # apply persona rewrite
    persona_template = get_persona_prompt(persona)

    rewrite_prompt = f"""
You rewrite responses into a defined personality voice.

Persona specification:
{persona_template}

Original response:
\"\"\"{base_response}\"\"\"

User memory profile:
{json.dumps(memory, indent=2)}

Rewrite Objective:
→ Same meaning, same advice outcome
→ NEW tone, pacing, voice, framing and attitude according to persona

Mandatory transformation rules:
1. Maintain factual meaning of the original answer.
2. Amplify persona traits — attitude, metaphors, rhythm, emotional tone.
3. PERSONALIZE using memory:
   - reference their habits, learning style, impatience, humor, etc.
4. Make the result feel like it was written FOR THIS USER, not for “users in general”.

Do NOT:
- Remove useful insights from base response
- Paraphrase lazily
- Revert to neutrality — commit to persona voice

Output ONLY rewritten persona-styled response.
"""

    persona_response = client.chat.completions.create(
        model="gpt-5-chat-latest",
        messages=[
            {"role": "system", "content": "You rewrite responses in different personality styles."},
            {"role": "user", "content": rewrite_prompt}
        ],
        response_format={"type": "text"}
    ).choices[0].message.content

    return base_response, persona_response