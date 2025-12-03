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
    You are an AI assistant.
    You have access to the user's long‑term memory:
    {json.dumps(memory, indent=2)}

    Respond to the user's message factually without tone styling.
    Tailor your response using their preferences, emotional tendencies, and learning style derived from memory.
    You MUST explicitly incorporate the user's stored memory.
    Reference their preferences, motivations, frustrations, tone tendencies, or learning style whenever appropriate.
    If the memory provides relevant insight, it MUST influence the wording, framing, and advice.
    Do NOT give generic or universal guidance — responses MUST feel customized to the user's identity.

    User: {user_message}
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
    Rewrite the following response using the described tone style.

    Persona Style:
    {persona_template}

    Original Response:
    {base_response}

    You MUST explicitly personalize the rewritten output using the user's stored memory below:
    {json.dumps(memory, indent=2)}

    Requirements:
    - Reference at least one user preference, frustration pattern, motivation trigger, or learning tendency.
    - The rewritten output MUST feel like it was crafted specifically for this user's personality.
    - Generic persona styling without personalization is unacceptable.
    - If necessary, rewrite until these conditions are met.

    Output rewritten response:
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