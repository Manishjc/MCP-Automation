from fastapi import FastAPI, Query
import requests
import google.generativeai as genai
import os
from datetime import datetime

# -----------------------------------------------------------
# Environment variables (set in Railway dashboard)
# -----------------------------------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FOOTBALL_KEY = os.getenv("FOOTBALL_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")

print("✅ GOOGLE_API_KEY Loaded:", GOOGLE_API_KEY is not None)

# -----------------------------------------------------------
# FASTAPI APP SETUP
# -----------------------------------------------------------
app = FastAPI(
    title="Simulated MCP Server",
    description="Provides Weather, Live Scores & Career Counselling via Gemini AI"
)

# -----------------------------------------------------------
# GEMINI AI CONFIGURATION
# -----------------------------------------------------------
genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------------------------------------------
# WEATHER TOOL
# -----------------------------------------------------------
@app.get("/weather")
def get_weather(city: str):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
        else:
            return {"error": f"Failed to fetch weather for {city}"}
    except Exception as e:
        return {"error": str(e)}

# -----------------------------------------------------------
# FOOTBALL SCORES TOOL
# -----------------------------------------------------------
@app.get("/score")
def get_scores(team_name: str):
    try:
        headers = {"x-apisports-key": FOOTBALL_KEY}

        # Get team ID
        team_search_url = "https://v3.football.api-sports.io/teams"
        search_params = {"search": team_name}
        team_resp = requests.get(team_search_url, headers=headers, params=search_params)

        if team_resp.status_code != 200:
            return {"error": f"Could not search team (HTTP {team_resp.status_code})"}

        teams = team_resp.json().get("response", [])
        if not teams:
            return {"message": f"No team found with name '{team_name}'"}

        team_id = teams[0]["team"]["id"]
        team_actual_name = teams[0]["team"]["name"]

        # Fetch last 5 matches
        fixtures_url = "https://v3.football.api-sports.io/fixtures"
        fixtures_params = {
            "team": team_id,
            "season": datetime.now().year,
            "last": 5
        }
        fixtures_resp = requests.get(fixtures_url, headers=headers, params=fixtures_params)

        if fixtures_resp.status_code != 200:
            return {"error": f"Could not fetch fixtures (HTTP {fixtures_resp.status_code})"}

        matches_data = fixtures_resp.json().get("response", [])
        if not matches_data:
            return {"message": f"No matches found for '{team_actual_name}'"}

        matches = []
        for match in matches_data:
            home_team = match["teams"]["home"]["name"]
            away_team = match["teams"]["away"]["name"]
            score_home = match["goals"]["home"]
            score_away = match["goals"]["away"]
            status = match["fixture"]["status"]["short"]
            match_date_iso = match["fixture"]["date"]
            match_date = datetime.fromisoformat(match_date_iso[:-1]).strftime("%d %b %Y")

            if team_actual_name.lower() in home_team.lower():
                opponent = away_team
                team_score = score_home
                opponent_score = score_away
            else:
                opponent = home_team
                team_score = score_away
                opponent_score = score_home

            if team_score > opponent_score:
                result = "Win"
            elif team_score < opponent_score:
                result = "Loss"
            else:
                result = "Draw"

            matches.append({
                "opponent": opponent,
                "score": f"{score_home} - {score_away}",
                "result": result,
                "status": status,
                "date": match_date
            })

        return {
            "team": team_actual_name,
            "last_5_matches": matches
        }

    except Exception as e:
        return {"error": str(e)}

# -----------------------------------------------------------
# IKIGAI CAREER COUNSELLOR TOOL
# -----------------------------------------------------------
@app.get("/ikigai")
def get_ikigai(love: str, good_at: str, world_needs: str, paid_for: str):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        You are an AI career counsellor using the Ikigai framework.
        User's answers:
        - Love: {love}
        - Good at: {good_at}
        - World needs: {world_needs}
        - Paid for: {paid_for}
        Provide a short, encouraging career recommendation (2-3 sentences).
        """
        response = model.generate_content(prompt)
        return {"ikigai_output": response.text}
    except Exception as e:
        return {"error": str(e)}

# -----------------------------------------------------------
# ROOT ENDPOINT
# -----------------------------------------------------------
@app.get("/")
def root():
    return {"message": "✅ MCP Server is running with Weather, Football & Career Counsellor tools."}


