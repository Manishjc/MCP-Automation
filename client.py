import requests

SERVER_URL = "http://127.0.0.1:8000"

def get_weather(city: str):
    url = f"{SERVER_URL}/weather"
    params = {"city": city}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        if "error" in data:
            print("❌", data["error"])
        else:
            print(f"🌦️ Weather in {data['city']}:")
            print(f"Temperature: {data['temperature']}")
            print(f"Description: {data['description']}")
    else:
        print("❌ Failed to fetch weather data.")

def get_scores(league_id: int):
    url = f"{SERVER_URL}/football"
    params = {"league_id": league_id}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        if "error" in data:
            print("❌", data["error"])
        else:
            print(f"⚽ Live Scores for League ID {league_id}:")
            for match in data.get("matches", []):
                print(f"{match['home_team']} {match['score']} {match['away_team']} [{match['status']}]")
            print()
    else:
        print("❌ Failed to fetch live scores.")

def get_ikigai():
    print("\n🌸 Welcome to the Ikigai Career Counsellor 🌸\n")
    love = input("❤️ What do you love doing? ")
    good_at = input("💪 What are you good at? ")
    world_needs = input("🌍 What does the world need? ")
    paid_for = input("💰 What can you be paid for? ")

    url = f"{SERVER_URL}/ikigai"
    params = {
        "love": love,
        "good_at": good_at,
        "world_needs": world_needs,
        "paid_for": paid_for
    }

    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            if "error" in data:
                print("❌ Error:", data["error"])
            else:
                print("\n💡 Your Ikigai Career Advice:\n")
                print(data["ikigai_output"])
        else:
            print("❌ Something went wrong.")
    except Exception as e:
        print("❌ Exception:", e)

if __name__ == "__main__":
    print("\n🌐 Welcome to MCP Client")
    print("1️⃣ Get Weather Updates")
    print("2️⃣ Get Live Football Scores")
    print("3️⃣ AI Career Counsellor (Ikigai)\n")

    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        city = input("Enter city name for weather: ")
        get_weather(city)
    elif choice == "2":
        league = int(input("Enter league ID for live scores (e.g., 39 for Premier League): "))
        get_scores(league)
    elif choice == "3":
        get_ikigai()
    else:
        print("❌ Invalid choice. Please choose between 1-3.")
