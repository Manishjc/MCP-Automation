import streamlit as st
import requests

# FastAPI backend URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="MCP Assistant 🌐", page_icon="🤖", layout="centered")

# Sidebar Navigation
st.sidebar.title("🌐 MCP Dashboard")
choice = st.sidebar.radio(
    "Choose a service:",
    ["🏙️ Weather Updates", "⚽ Live Football Scores", "🌸 Ikigai Career Counsellor"]
)

st.title("🤖 Multi-purpose Assistant (MCP)")
st.markdown("Get **Weather**, **Football Scores**, or **Career Guidance** in one place!")

# --------------------------
# WEATHER SECTION
# --------------------------
if choice == "🏙️ Weather Updates":
    st.header("☀️ Get Real-Time Weather Updates")

    city = st.text_input("Enter your city name:")
    if st.button("Get Weather"):
        if city.strip() == "":
            st.warning("⚠️ Please enter a city name.")
        else:
            try:
                response = requests.get(f"{BASE_URL}/weather", params={"city": city}, timeout=20)
                data = response.json()

                if "error" in data:
                    st.error(f"❌ {data['error']}")
                else:
                    st.success(f"🌤️ Weather in **{city.title()}**")
                    st.write(f"**Temperature:** {data['temperature']}°C")
                    st.write(f"**Condition:** {data['description']}")
            except Exception as e:
                st.error(f"⚠️ Could not connect to server. Error: {e}")

# --------------------------
# FOOTBALL SCORES SECTION
# --------------------------
elif choice == "⚽ Live Football Scores":
    st.header("⚽ Get Live Football Scores")

    team = st.text_input("Enter team name:")
    if st.button("Get Scores"):
        if team.strip() == "":
            st.warning("⚠️ Please enter a team name.")
        else:
            try:
                response = requests.get(f"{BASE_URL}/score", params={"team": team}, timeout=20)
                data = response.json()

                if "error" in data:
                    st.error(f"❌ {data['error']}")
                else:
                    st.success(f"📊 Match Update for {team.title()}:")
                    st.write(f"🏟️ **Opponent:** {data['opponent']}")
                    st.write(f"🔢 **Score:** {data['score']}")
                    st.write(f"⏱️ **Status:** {data['status']}")
            except Exception as e:
                st.error(f"⚠️ Could not connect to server. Error: {e}")

# --------------------------
# IKIGAI CAREER COUNSELLOR SECTION
# --------------------------
elif choice == "🌸 Ikigai Career Counsellor":
    st.header("🌸 AI Career Counsellor — Find Your Ikigai")

    love = st.text_input("❤️ What do you love doing?")
    good_at = st.text_input("💪 What are you good at?")
    world_needs = st.text_input("🌍 What does the world need?")
    paid_for = st.text_input("💰 What can you be paid for?")

    if st.button("✨ Get My Ikigai Recommendation"):
        if not all([love, good_at, world_needs, paid_for]):
            st.warning("⚠️ Please fill in all four fields.")
        else:
            with st.spinner("Thinking deeply about your purpose... 💭"):
                try:
                    response = requests.get(
                        f"{BASE_URL}/ikigai",
                        params={
                            "love": love,
                            "good_at": good_at,
                            "world_needs": world_needs,
                            "paid_for": paid_for
                        },
                        timeout=30
                    )
                    data = response.json()

                    if "ikigai_output" in data:
                        st.success("🌟 Here's your Ikigai Career Suggestion:")
                        st.markdown(f"**{data['ikigai_output']}**")
                    else:
                        st.error(f"❌ Error: {data.get('error', 'Unknown issue')}")
                except Exception as e:
                    st.error(f"⚠️ Could not connect to server. Error: {e}")
