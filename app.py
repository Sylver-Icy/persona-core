import streamlit as st
from core.memory_extractor import extract_memory
from core.generator import generate_reply
from test import DEFAULT_MESSAGES
import time

st.set_page_config(page_title="PersonaCore AI", layout="centered")

st.title("👋 Hiiii, I'm your Personality-Aware AI Friend")

st.write(
    """
I learn about you from your chat history and then talk to you in different styles—
like a mentor, roaster, therapist, or chaotic best friend
"""
)

#ask if user wants to upload their own chat history
choice = st.selectbox(
    "Do you want to insert your own chat history?",
    ["No, use demo data", "Yes, upload mine"]
)

#collect or use default messages
if choice == "Yes, upload mine":
    st.subheader("✍️ Paste 20-30 chat messages about you")
    st.caption("Keep it under 1500 characters — no books 😭")
    raw_input = st.text_area("Chat History", max_chars=1500)

    if st.button("Extract My Memory"):
        if len(raw_input.strip()) < 250:
            st.warning("that’s like 2 sentences 💀 give me more context.")
        else:
            messages = [line.strip() for line in raw_input.split("\n") if line.strip()]
            with st.spinner("🤔 Hmmm, let me read through our chats real quick..."):
                st.session_state.memory = extract_memory(messages)
            st.success("Memory learned! 🧠")
            st.json(st.session_state.memory)

else:
    if st.button("Load Demo Memory"):
        with st.spinner("🤔 Hmmm, let me skim this demo lore real quick..."):
            st.session_state.memory = extract_memory(DEFAULT_MESSAGES)
        st.success("Demo memory loaded! 🧠")
        st.json(st.session_state.memory)

#Persona Selection
st.subheader("🤝 Pick what kind of friend I should be to you")

persona = st.selectbox(
    "Who am I today?",
    ["mentor", "witty_friend", "therapist", "roaster", "teacher"]
)

#Chat Section
st.subheader("💬 Okay let's talk!")

# rate limit: per-session usage counter
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

# rate limit: cooldown timer
if "last_call" not in st.session_state:
    st.session_state.last_call = 0

user_query = st.text_input("Say something…")

if st.button("Respond"):
    if "memory" not in st.session_state:
        st.warning("YO you haven't fed me your lore yet. Extract memory first.")
    else:
        # cooldown check
        now = time.time()
        if now - st.session_state.last_call < 3:
            st.warning("Relax friend... I'm still typing, wait a sec.")
            st.stop()
        st.session_state.last_call = now

        # usage cap check
        if st.session_state.usage_count >= 10:
            st.error("⚠️ Free trial over bro 😭 DM the dev for more tokens.")
            st.stop()

        st.session_state.usage_count += 1

        with st.spinner("⌨️ typing..."):
            base, styled = generate_reply(user_query, persona, st.session_state.memory)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🤖 Before Personality Engine")
            st.write(base)
        with col2:
            st.markdown(f"### 🎭 After applying **{persona}** personality")
            st.write(styled)