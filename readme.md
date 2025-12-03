# PersonaCore 🧠🎭
Memory-driven personality engine for agentic AI

PersonaCore is a small demo that shows how an AI agent can:

- Extract long-term **user memory** from chat history
- Remember **preferences, emotional patterns, and facts**
- Apply a **Personality Engine** (mentor, roaster, therapist, etc.)
- Show **before/after** replies to prove tone transformation

Built for an AI Engineer assignment focused on memory, tone, and modular design.

---

## 🔧 What it does

### 🧠 Memory Extraction
Given ~20–30 chat messages, the system:

- Parses user **likes / dislikes**
- Detects **emotional patterns** (rage, burnout, humor, impatience, etc.)
- Pulls out **facts worth remembering** (goals, style, habits)

Output is a **structured JSON memory object** that other modules can use.

---

### 🎭 Personality Engine

PersonaCore supports multiple personas:

- `mentor` – calm, structured, guiding
- `witty_friend` – chaotic, slangy, teasing
- `therapist` – warm, validating, reflective
- `roaster` – brutal honest, sarcastic but helpful
- `teacher` – analogy-heavy, step-by-step explainer

Each persona has **rule-based prompt instructions** that control:
- Tone
- Word choice
- Attitude
- Style of explanation

---

### 🔁 Before / After Responses

For every user query, the system generates:

1. **Base response**
   - Neutral, factual answer using the stored memory

2. **Persona-styled response**
   - Same answer, but rewritten in the selected persona’s voice

Both are shown **side by side** in the UI.

---

### 💻 Streamlit UI

The Streamlit app (`app.py`) handles:

1. **Onboarding text** (“Hiiii, I’m your personality-aware AI friend…”)
2. **Chat history input**
   - User can paste their own messages
   - Or use built-in demo data
   - Input length is capped to avoid token spam
3. **Memory extraction**
   - Displays extracted memory as JSON
4. **Persona selection**
   - Dropdown: mentor / witty_friend / therapist / roaster / teacher
5. **Chat panel**
   - User types a message
   - App shows **Before Personality Engine** and **After applying persona** side by side

---

### 🛡 Token & Abuse Protection

Since this uses a real OpenAI API key, PersonaCore includes:

- **Per-session usage cap:**
  - After 10 responses: shows
    > “⚠️ Free trial over bro”
- **Cooldown between requests:**
  - 3s minimum gap, or it says:
    > “Relax friend... I'm still typing, wait a sec.”
- **Input limits:**
  - Chat history and query size are capped

This keeps the demo from nuking the API bill.

---

## 🧱 Project Structure

```text
PersonaCore/
├─ core/
│  ├─ memory_extractor.py   # LLM memory extraction → structured JSON
│  ├─ persona_engine.py     # Persona templates + tone rules
│  ├─ generator.py          # Base reply + persona rewrite + memory grounding
├─ app.py                   # Streamlit UI + pipeline glue
├─ test.py                  # Local test harness + DEFAULT_MESSAGES demo history
└─ README.md