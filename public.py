import streamlit as st
import pandas as pd

# Load the auction and bid data CSV files (only once per session)
@st.cache_data
def load_data():
    auction_df = pd.read_csv('auction.csv')
    players_bids_df = pd.read_csv('players_bids.csv')
    return auction_df, players_bids_df

# Public page
def public_page():
    st.title("IPL Auction 2024")
    st.subheader("Bid Amounts by Team")

    # Define the total budget for each team
    total_budget = 120  # 120 crores

    # Add a refresh button to reload the data from the CSV
    if st.button("Refresh Data"):
        st.session_state.players_bids_df = pd.read_csv('players_bids.csv')

    # Get the list of unique teams from the bid data
    teams = st.session_state.players_bids_df['Franchise'].unique()

    # Dropdown to select a team
    selected_team = st.selectbox("Select a Team", teams)

    # Filter players by selected team
    team_players = st.session_state.players_bids_df[st.session_state.players_bids_df['Franchise'] == selected_team]
    
    # Display team name and player bids
    st.subheader(f"Team: {selected_team}")
    st.dataframe(team_players[['Player Name', 'Bid Amount']])

    # Calculate the sum of the bid amounts for the current team
    total_bid_amount = team_players['Bid Amount'].sum()

    # Calculate the remaining budget
    remaining_budget = total_budget - total_bid_amount

    # Display the remaining budget
    st.write(f"Remaining Budget: ₹{remaining_budget} Crores")

# Main function to handle the page
def main():
    # Load the data only once at the start of the session
    if 'players_bids_df' not in st.session_state:
        _, players_bids_df = load_data()
        st.session_state.players_bids_df = players_bids_df

    # Public page content
    public_page()

if __name__ == "__main__":
    main()
