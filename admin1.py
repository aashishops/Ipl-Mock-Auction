from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load data (simulate cache)
auction_df = pd.read_csv("mock_auction_players.csv")
players_bids_df = pd.read_csv("players_bids.csv")

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Render admin dashboard."""
    available_players = auction_df[~auction_df['Player Name'].isin(
        players_bids_df[players_bids_df['Bid Amount'] > 0]['Player Name']
    )]
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "players": available_players.to_dict(orient="records"),
        "teams": [
            'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore', 'Delhi Capitals',
            'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Rajasthan Royals', 'Punjab Kings',
            'Lucknow Super Giants', 'Gujarat Titans', 'Unsold'
        ]
    })

@app.post("/update_bid")
async def update_bid(
    player_name: str = Form(...),
    team_name: str = Form(...),
    bid_amount: int = Form(...)
):
    """Handle bid updates."""
    global players_bids_df  # Reference the global dataframe

    # Get player data
    player_data = auction_df[auction_df['Player Name'] == player_name].iloc[0]
    player_role = player_data["Role"]
    player_points = player_data["Points"]

    # Check and update bids
    if not players_bids_df[(players_bids_df["Player Name"] == player_name) &
                           (players_bids_df["Franchise"] == team_name)].empty:
        # Update existing record
        players_bids_df.loc[(players_bids_df["Player Name"] == player_name) &
                            (players_bids_df["Franchise"] == team_name), "Bid Amount"] = bid_amount
    else:
        # Add new record
        new_row = pd.DataFrame([{
            "Player Name": player_name,
            "Franchise": team_name,
            "Bid Amount": bid_amount,
            "Role": player_role,
            "Points": player_points
        }])
        players_bids_df = pd.concat([players_bids_df, new_row], ignore_index=True)

    # Save changes
    players_bids_df.to_csv("players_bids.csv", index=False)
    return RedirectResponse("/", status_code=303)
