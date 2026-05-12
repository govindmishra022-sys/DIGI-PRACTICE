import streamlit as st
from google import genai
from google.genai import types
import datetime
import random

# The client will be initialized dynamically based on user input.
client = None

# Configure the Streamlit page
st.set_page_config(page_title="Astrology Chatbot", page_icon="🕉️", layout="wide")

# Custom CSS for structural elements only (allowing native Dark/Light mode)
custom_css = """
<style>
    /* Aura Visualizer Gradient */
    .aura-box {
        height: 120px;
        border-radius: 15px;
        background: linear-gradient(135deg, #fdf4ff, #e879f9, #38bdf8);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Main Title
st.title("🕉️ Cosmic Guide: Advanced Astrology")
st.markdown("Your cultural and spiritual root map to the stars. Ask about Doshas, Panchang, Kundli, and your destiny.")

# Configuration Expander (Hidden when not in use)
with st.expander("⚙️ Settings & Configuration", expanded=True):
    col_api, col_lang = st.columns(2)
    with col_api:
        st.write("**🔑 API Settings**")
        user_api_key = st.text_input("Enter Gemini API Key", type="password", placeholder="AIzaSy...", key="api_key_input")
        if st.session_state.get("api_key_input"):
            client = genai.Client(api_key=st.session_state["api_key_input"])
    with col_lang:
        st.write("**🌐 Select Language / भाषा**")
        preferred_language = st.selectbox("Choose your language", ["English", "Hindi", "Marathi", "Gujarati", "Bengali", "Tamil", "Telugu", "Spanish", "French"], label_visibility="collapsed")

zodiac_signs = ["", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
zodiac_emojis = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

# Sidebar for personal details
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1532012197267-da84d127e765?auto=format&fit=crop&w=800&q=80", caption="Connect with your roots")
    st.header("🪔 Your Birth Details")
    user_name = st.text_input("Name", placeholder="E.g., Arjun")
    birth_date = st.date_input("Date of Birth", value=None, min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    birth_time = st.time_input("Time of Birth", value=None)
    birth_location = st.text_input("Place of Birth", placeholder="City, State")
    sun_sign = st.selectbox("Sun Sign / Surya Rashi", zodiac_signs)
    moon_sign = st.selectbox("Moon Sign / Chandra Rashi", zodiac_signs)

# Helper Functions
def generate_svg_kundli(sun, moon):
    houses = {i: [] for i in range(1, 13)}
    if sun:
        sun_idx = zodiac_signs.index(sun)
        houses[sun_idx if sun_idx <= 12 else 1].append("☀️ Sun")
    else:
        houses[1].append("☀️ Sun")
        
    if moon:
        moon_idx = zodiac_signs.index(moon)
        houses[(moon_idx + 3) % 12 + 1].append("🌙 Moon")
    else:
        houses[4].append("🌙 Moon")
        
    planets = ["Mars", "Merc", "Jup", "Ven", "Sat", "Rahu", "Ketu"]
    for p in planets:
        h = random.randint(1, 12)
        if len(houses[h]) < 3:
            houses[h].append(p)

    svg = f"""
<div style="display: flex; justify-content: center; margin: 20px 0;">
    <svg viewBox="0 0 400 400" style="width:100%; max-width: 350px;">
      <!-- Outer Box -->
      <rect x="10" y="10" width="380" height="380" fill="transparent" stroke="#ea580c" stroke-width="3"/>
      <!-- Diagonals -->
      <line x1="10" y1="10" x2="390" y2="390" stroke="#ea580c" stroke-width="2"/>
      <line x1="10" y1="390" x2="390" y2="10" stroke="#ea580c" stroke-width="2"/>
      <!-- Midpoint Diamond -->
      <line x1="200" y1="10" x2="390" y2="200" stroke="#ea580c" stroke-width="2"/>
      <line x1="390" y1="200" x2="200" y2="390" stroke="#ea580c" stroke-width="2"/>
      <line x1="200" y1="390" x2="10" y2="200" stroke="#ea580c" stroke-width="2"/>
      <line x1="10" y1="200" x2="200" y2="10" stroke="#ea580c" stroke-width="2"/>
      
      <!-- Text Placements (Houses 1 to 12 in North Indian Style) -->
      <text x="200" y="70" text-anchor="middle" font-size="12" font-weight="bold" fill="#ea580c">{', '.join(houses[1])}</text>
      <text x="100" y="50" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[2])}</text>
      <text x="50" y="100" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[3])}</text>
      <text x="120" y="200" text-anchor="middle" font-size="12" font-weight="bold" fill="#ea580c">{', '.join(houses[4])}</text>
      <text x="50" y="300" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[5])}</text>
      <text x="100" y="350" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[6])}</text>
      <text x="200" y="320" text-anchor="middle" font-size="12" font-weight="bold" fill="#ea580c">{', '.join(houses[7])}</text>
      <text x="300" y="350" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[8])}</text>
      <text x="350" y="300" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[9])}</text>
      <text x="280" y="200" text-anchor="middle" font-size="12" font-weight="bold" fill="#ea580c">{', '.join(houses[10])}</text>
      <text x="350" y="100" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[11])}</text>
      <text x="300" y="50" text-anchor="middle" font-size="10" fill="#ea580c">{', '.join(houses[12])}</text>
      
      <!-- House Numbers -->
      <text x="200" y="30" text-anchor="middle" font-size="14" fill="#9ca3af">1</text>
      <text x="100" y="30" text-anchor="middle" font-size="14" fill="#9ca3af">2</text>
      <text x="30" y="100" text-anchor="middle" font-size="14" fill="#9ca3af">3</text>
      <text x="80" y="200" text-anchor="middle" font-size="14" fill="#9ca3af">4</text>
      <text x="30" y="300" text-anchor="middle" font-size="14" fill="#9ca3af">5</text>
      <text x="100" y="380" text-anchor="middle" font-size="14" fill="#9ca3af">6</text>
      <text x="200" y="380" text-anchor="middle" font-size="14" fill="#9ca3af">7</text>
      <text x="300" y="380" text-anchor="middle" font-size="14" fill="#9ca3af">8</text>
      <text x="370" y="300" text-anchor="middle" font-size="14" fill="#9ca3af">9</text>
      <text x="320" y="200" text-anchor="middle" font-size="14" fill="#9ca3af">10</text>
      <text x="370" y="100" text-anchor="middle" font-size="14" fill="#9ca3af">11</text>
      <text x="300" y="30" text-anchor="middle" font-size="14" fill="#9ca3af">12</text>
    </svg>
</div>
"""
    return svg

def make_system_prompt():
    prompt = (
        "You are an expert Vedic astrologer. You provide deep, cultural, and spiritual guidance based on the user's birth details. "
        "Always structure your answers nicely. You must provide specific remedies for Doshas (like Mangal Dosh, Kalsarp Dosh, Sade Sati) if the user asks or if relevant. "
        "Recommend specific gemstones, colors, and metals to wear based on their Sun and Moon signs. "
        "Use traditional Indian cultural symbols (🕉️, 🪔, 🌸, 📿) in your responses."
    )
    if user_name: prompt += f"\nUser Name: {user_name}"
    if sun_sign: prompt += f"\nSun Sign (Surya Rashi): {sun_sign}"
    if moon_sign: prompt += f"\nMoon Sign (Chandra Rashi): {moon_sign}"
    if birth_date: prompt += f"\nDOB: {birth_date}"
    prompt += f"\n\n[CRITICAL]: The user has explicitly selected {preferred_language} as their preferred language. You MUST translate and write your ENTIRE response exclusively in {preferred_language}. Never use English unless English is selected."
    
    return prompt

st.markdown("---")
st.subheader("🌌 Cosmic Dashboards")

# Collapsible feature sections
with st.expander("📜 Your North Indian Kundli Chart"):
    st.markdown("Here is a diagrammatical representation of your planetary placements:")
    html_content = "".join(line.strip() for line in generate_svg_kundli(sun_sign, moon_sign).splitlines())
    st.markdown(html_content, unsafe_allow_html=True)

with st.expander("🛡️ Dosha Identification & Solutions"):
    st.markdown("Based on standard planetary placements, here is a quick overview of potential Doshas:")
    st.write("**🔥 Mangal Dosh (Kuja Dosha)**")
    st.write("Mars placement in 1st, 4th, 7th, 8th, or 12th house. *Remedy:* Chant Hanuman Chalisa, wear Coral (Moonga), or donate red lentils on Tuesdays.")
    st.write("**🐍 Kalsarp Dosh**")
    st.write("When all planets are hemmed between Rahu and Ketu. *Remedy:* Offer milk to Lord Shiva, chant Maha Mrityunjaya Mantra, wear a silver snake ring.")

with st.expander("💎 Lucky Cosmic Remedies & Aura"):
    st.write("**🌈 Auspicious Color:** Saffron or White to attract positive energy.")
    st.write("**💍 Favorable Metal:** Gold or Silver will balance your core vibrations.")
    st.write("**💎 Recommended Gem:** Ruby or Pearl on your right hand to strengthen your ruling planets.")
    st.markdown("---")
    st.write("**✨ Your Aura Visualizer:** Your energetic signature based on today's transits:")
    st.markdown("<div class='aura-box'>Ethereal Gold & Violet Aura</div>", unsafe_allow_html=True)
    st.info("🎵 **Recommended Frequency:** Listen to 528Hz (The Love/Miracle Frequency) today to cleanse your aura.")

with st.expander("📅 Today's Panchang (Almanac)"):
    st.write(f"**Date:** {datetime.date.today().strftime('%B %d, %Y')}")
    st.write("- **Tithi (Lunar Day):** Shukla Paksha Dashami")
    st.write("- **Nakshatra (Constellation):** Rohini")
    st.write("- **Yoga:** Siddhi")
    st.write("- **Karana:** Taitila")
    st.caption("*(Note: This is a generated sample Panchang for demonstration purposes. Ask the Chatbot for precise transit data!)*")

st.markdown("---")

# Persistent Chatbot Interface at the bottom
st.subheader("💬 Consult the Spiritual Guide")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your Kundli, Doshas, or future..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    system_prompt = make_system_prompt()
    conversation_text = ""
    for msg in st.session_state.messages:
        role_name = "User" if msg["role"] == "user" else "Astrologer"
        conversation_text += f"{role_name}: {msg['content']}\n"
    conversation_text += "Astrologer: "

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if not client:
            st.error("Please enter your Google Gemini API Key in the Settings & Configuration section at the top to consult the spiritual guide.")
        else:
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=conversation_text,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                    )
                )
                response_text = response.text
                message_placeholder.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Failed to communicate with the spirits: {e}")
