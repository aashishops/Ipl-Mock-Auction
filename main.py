from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Dictionary with IPL team usernames and passwords
team_credentials = {
    "Mumbai Indians": "mi@2024",
    "Chennai Super Kings": "csk@2024",
    "Delhi Capitals": "dc@2024",
    "Kolkata Knight Riders": "kkr@2024",
    "Royal Challengers Bangalore": "rcb@2024",
    "Royal Rajasthan": "rr@2024",
    "Sunrisers Hyderabad": "srh@2024",
    "Punjab Kings": "pbks@2024",
    "Lucknow Super Giants": "lsg@2024",
    "Gujarat Titans": "gt@2024"
}

# Load the player bid data
players_df = pd.read_csv('players_bids.csv')

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "teams": team_credentials.keys()})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, team_name: str = Form(...), password: str = Form(...)):
    if team_credentials.get(team_name) == password:
        team_players = players_df[players_df['Franchise'] == team_name]['Player Name'].tolist()
        return templates.TemplateResponse("index.html", {"request": request, "team_name": team_name, "team_players": team_players})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "teams": team_credentials.keys(), "error": "Invalid username or password. Please try again."})

@app.post("/submit_team", response_class=HTMLResponse)
async def submit_team(request: Request, team_name: str = Form(...), selected_players: list[str] = Form(...)):
    team_players = players_df[players_df['Franchise'] == team_name]
    selected_team_df = team_players[team_players['Player Name'].isin(selected_players)]
    selected_team_df = selected_team_df[['Player Name', 'Franchise', 'Points', 'Role']]

    # Define CSV file path
    csv_file = 'final_team.csv'

    # Append data to the CSV file
    if os.path.exists(csv_file):
        selected_team_df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        selected_team_df.to_csv(csv_file, mode='w', header=True, index=False)

  
    average_points = selected_team_df['Points'].mean()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "team_name": team_name,
        "selected_team_df": selected_team_df.to_html(classes='data', header="true"),
        "average_points": average_points
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)