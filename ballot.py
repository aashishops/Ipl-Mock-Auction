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
    "Rajasthan Royals": "rr@2024",
    "Sunrisers Hyderabad": "srh@2024",
    "Punjab Kings": "pbks@2024",
    "Lucknow Super Giants": "lsg@2024",
    "Gujarat Titans": "gt@2024"
}

# Load the player bid data
players_df = pd.read_csv('legends.csv')

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("ballot.html", {
        "request": request,
        "teams": team_credentials.keys(),
        "players": players_df['Player Name'].unique()
    })

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, team_name: str = Form(...), password: str = Form(...)):
    if team_credentials.get(team_name) == password:
        return templates.TemplateResponse("ballot.html", {
            "request": request,
            "team_name": team_name,
            "players": players_df['Player Name'].unique()
        })
    else:
        return templates.TemplateResponse("ballot.html", {
            "request": request,
            "teams": team_credentials.keys(),
            "error": "Invalid username or password. Please try again."
        })

@app.post("/submit_bid", response_class=HTMLResponse)
async def submit_bid(request: Request, team_name: str = Form(...), player_name: str = Form(...), bid_amount: float = Form(...)):
    # Define the CSV file path
    ballot_file = 'secret_ballot.csv'

    # Append data to the CSV file
    new_row = pd.DataFrame({
        'Franchise': [team_name],
        'Player Name': [player_name],
        'Bid Amount': [bid_amount]
    })

    if os.path.exists(ballot_file):
        new_row.to_csv(ballot_file, mode='a', header=False, index=False)
    else:
        new_row.to_csv(ballot_file, mode='w', header=True, index=False)

    return templates.TemplateResponse("ballot.html", {
        "request": request,
        "team_name": team_name,
        "players": players_df['Player Name'].unique(),
        "success": f"Your bid for {player_name} has been recorded."
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=4201)
