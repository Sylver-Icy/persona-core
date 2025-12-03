from core.memory_extractor import extract_memory

messages = [
    "Man today sucked, failed an exam and tilted instantly.",
    "Ended up grinding Valorant for 6 hours straight to cool off.",
    "Bro I swear when code doesn't work I rage more than in ranked.",
    "I'm studying engineering but it feels like I'm speedrunning depression.",
    "Honestly I'd rather build AI projects than study theory I'm just built different.",
    "History lectures make me sleepy, like actual coma." ,
    "Sarcasm is my first language.",
    "Roast me sometimes, it weirdly motivates me.",
    "Watched some anime at 3am because sleep is for casuals.",
    "Formal people annoy me, talk like humans please.",
    "Pulled an all‑nighter coding again — coffee is holding me hostage.",
    "Theory lectures are torture, who designs this garbage?",
    "I learn best by doing, not reading some 200 page notes.",
    "Whenever my code fails I full rage but still come back like a toxic ex.",
    "Music hits different when debugging.",
    "Waiting for replies is physical pain, why is everyone slow.",
    "Dark humor is elite, don't judge me.",
    "Slow internet should be a war crime.",
    "Tried a hacking challenge today — fun as hell.",
    "Messing with AI models is my version of playground.",
    "If something is boring I drop it instantly, attention span = goldfish.",
    "I love problem solving when it's actually interesting.",
    "Textbook reading feels like slowly dying.",
    "Debugging is painful but also spicy fun sometimes.",
    "Gaming marathons >>> social life.",
    "People who talk too formally give me trust issues.",
    "If I don't feel engaged I just mentally uninstall.",
    "I respect mentors who roast me — keeps me sharp.",
    "I want to build cool shit, not memorize garbage.",
    "Low‑key I believe tech will be my escape arc.",
]

# Ensure you pass a list of strings (like 30 msgs IRL)
print("🔍 Sending messages for extraction...\n")

memory = extract_memory(messages)

print("📌 Extracted Memory:")
print(memory)