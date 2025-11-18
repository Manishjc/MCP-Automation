from fastapi import FastAPI, Query, Form
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv 

import datetime
current_year = datetime.datetime.now().year
season = current_year 


load_dotenv()
print("✅ GOOGLE_API_KEY Loaded:", os.getenv("GOOGLE_API_KEY") is not None)

# -----------------------------------------------------------
# 🔹 FASTAPI APP SETUP
# -----------------------------------------------------------
app = FastAPI(
    title="Simulated MCP Server",
    description="Provides Weather, Live Scores & Career Counselling via Gemini AI"
)

# -----------------------------------------------------------
# 🔹 GEMINI AI CONFIGURATION
# -----------------------------------------------------------
# ✅ Either set environment variable or paste key directly here
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
genai.configure(api_key="AIzaSyBISBL4-8_hJZAsyJ_nO6B4CKDokXESIRQ")  # Replace with your Gemini API key

# -----------------------------------------------------------
# 🔹 WEATHER TOOL (GET)
# -----------------------------------------------------------


@app.get("/weather")
def get_weather(city: str):
    try:
        import requests
        api_key = "5628c7ba900a3698815f757559fabcd8"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
            return weather
        else:
            return {"error": f"Failed to fetch weather for {city}"}
    except Exception as e:
        return {"error": str(e)}


# -----------------------------------------------------------
# 🔹 LIVE FOOTBALL SCORES TOOL (GET)
# -----------------------------------------------------------
FOOTBALL_KEY = "80f480d6ec6598ab5148c948b17a5061"


from datetime import datetime

# -----------------------------------------------------------
# 🔹 LIVE FOOTBALL SCORES TOOL (GET) - LAST 5 MATCHES (USER-FRIENDLY + FORMATTED DATE)
# -----------------------------------------------------------
FOOTBALL_KEY = "80f480d6ec6598ab5148c948b17a5061"

@app.get("/score")
def get_scores(team_name: str):
    """
    MCP Tool: Fetch the last 5 football matches and results for a given team name with formatted dates.
    """
    try:
        headers = {"x-apisports-key": FOOTBALL_KEY}

        # Step 1: Get team ID from team name
        team_search_url = "https://v3.football.api-sports.io/teams"
        search_params = {"search": team_name}
        team_resp = requests.get(team_search_url, headers=headers, params=search_params)

        if team_resp.status_code != 200:
            return {"error": f"Could not search team (HTTP {team_resp.status_code})"}

        teams = team_resp.json().get("response", [])
        if not teams:
            return {"message": f"No team found with name '{team_name}'"}

        team_id = teams[0]["team"]["id"]  # pick the first match
        team_actual_name = teams[0]["team"]["name"]

        # Step 2: Fetch last 5 matches using team ID
        fixtures_url = "https://v3.football.api-sports.io/fixtures"
        fixtures_params = {
            "team": team_id,
            "season": 2025,
            "last": 5
        }
        fixtures_resp = requests.get(fixtures_url, headers=headers, params=fixtures_params)

        if fixtures_resp.status_code != 200:
            return {"error": f"Could not fetch fixtures (HTTP {fixtures_resp.status_code})"}

        matches_data = fixtures_resp.json().get("response", [])
        if not matches_data:
            return {"message": f"No matches found for '{team_actual_name}'"}

        # Step 3: Process matches
        matches = []
        for match in matches_data:
            home_team = match["teams"]["home"]["name"]
            away_team = match["teams"]["away"]["name"]
            score_home = match["goals"]["home"]
            score_away = match["goals"]["away"]
            status = match["fixture"]["status"]["short"]
            match_date_iso = match["fixture"]["date"]

            # Format date to "DD MMM YYYY"
            match_date = datetime.fromisoformat(match_date_iso[:-1]).strftime("%d %b %Y")

            # Identify opponent and team's score
            if team_actual_name.lower() in home_team.lower():
                opponent = away_team
                team_score = score_home
                opponent_score = score_away
            else:
                opponent = home_team
                team_score = score_away
                opponent_score = score_home

            # Determine result
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
# 🔹 CAREER COUNSELLOR TOOL (POST)
# -----------------------------------------------------------
@app.get("/ikigai")
def get_ikigai(love: str, good_at: str, world_needs: str, paid_for: str):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are an AI career counsellor using the Ikigai framework.
        Here are the user's answers:
        - What they love: {love}
        - What they are good at: {good_at}
        - What the world needs: {world_needs}
        - What they can be paid for: {paid_for}

        Based on this, provide a short, encouraging career recommendation (2-3 sentences).
        """

        response = model.generate_content(prompt)
        return {"ikigai_output": response.text}

    except Exception as e:
        return {"error": str(e)}


# -----------------------------------------------------------
# 🔹 ROOT ENDPOINT
# -----------------------------------------------------------
@app.get("/")
def root():
    return {"message": "✅ MCP Server is running with Weather, Football & Career Counsellor tools."}
