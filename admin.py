import streamlit as st
import pandas as pd

# Load the auction and bid data CSV files (only once per session)
@st.cache_data
def load_data():
    auction_df = pd.read_csv('mock_auction_players.csv')
    players_bids_df = pd.read_csv('players_bids.csv')
    return auction_df, players_bids_df

IPL_FRANCHISES = [
    'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore', 'Delhi Capitals',
    'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Rajasthan Royals', 'Punjab Kings',
    'Lucknow Super Giants', 'Gujarat Titans', 'Unsold'
]

def update_bid(player_name, team_name, bid_amount):
    # Access the DataFrame from session state
    players_bids_df = st.session_state.players_bids_df
    auction_df = st.session_state.auction_df  # Get auction data

    # Extract the player role and points from auction_df
    player_data = auction_df[auction_df['Player Name'] == player_name].iloc[0]
    player_role = player_data['Role']
    player_points = player_data['Points']
    
    # Check if the player and team are already in the dataframe
    if not players_bids_df[(players_bids_df['Player Name'] == player_name) & 
                            (players_bids_df['Franchise'] == team_name)].empty:
        # Update the bid amount for the specific player and team
        players_bids_df.loc[(players_bids_df['Player Name'] == player_name) & 
                             (players_bids_df['Franchise'] == team_name), 'Bid Amount'] = bid_amount
    else:
        # If no record found, add a new row for the player and team along with role and points
        new_row = pd.DataFrame([{'Player Name': player_name, 'Franchise': team_name, 'Bid Amount': bid_amount,
                                 'Role': player_role, 'Points': player_points}])
        players_bids_df = pd.concat([players_bids_df, new_row], ignore_index=True)

    # Save the updated dataframe to CSV (only the bid update)
    players_bids_df.to_csv('players_bids.csv', index=False)
    
    # Update session state with new data to reflect changes on the page
    st.session_state.players_bids_df = players_bids_df  # Re-assign the updated DataFrame to session state
    # Keep the auction data intact, no need to reload auction data

# Admin page
def admin_page():
    st.title("Admin Dashboard")
    st.subheader("Manage Player Bids")

    # Re-load the available players after bid update
    available_players = st.session_state.auction_df[~st.session_state.auction_df['Player Name'].isin(
        st.session_state.players_bids_df[st.session_state.players_bids_df['Bid Amount'] > 0]['Player Name']
    )]

    # Let admin select a player to update the bid
    if not available_players.empty:
        player_name = st.selectbox("Select Player", available_players['Player Name'])
        team_name = st.selectbox("Select Team", IPL_FRANCHISES)
        bid_amount = st.number_input(f"Enter Bid Amount for {player_name} ({team_name})", min_value=0, value=0)

        st.text(f"Counter: {st.session_state.counter}")

        # Update bid button
        if st.button("Update Bid", key="update_bid_button"):
            if bid_amount > 0:
                update_bid(player_name, team_name, bid_amount)
                st.success(f"Updated bid for {player_name} in {team_name} to ₹{bid_amount} Lakh")
                # Reload available players after update (without reloading the whole auction)
                available_players = st.session_state.auction_df[~st.session_state.auction_df['Player Name'].isin(
                    st.session_state.players_bids_df[st.session_state.players_bids_df['Bid Amount'] > 0]['Player Name']
                )]  # Update available players list
                st.success("Data reloaded successfully.")
                st.session_state.counter += 1
            else:
                st.error("Bid amount must be greater than zero")
    else:
        st.write("All players have been bid on.")
    

# Main function to handle the page
def main():
    # Load the data only once at the start of the session
    if 'auction_df' not in st.session_state or 'players_bids_df' not in st.session_state:
        auction_df, players_bids_df = load_data()
        st.session_state.auction_df = auction_df
        st.session_state.players_bids_df = players_bids_df

    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    # Admin page content
    admin_page()

if __name__ == "__main__":
    main()
