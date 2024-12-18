import streamlit as st
import pandas as pd

# Load the auction and bid data CSV files (only once per session)
@st.cache_data
def load_data():
    auction_df = pd.read_csv('mock_auction_players.csv')
    players_bids_df = pd.read_csv('final_team.csv')
    return auction_df, players_bids_df

# Public page
def public_page():
    st.title("IPL Auction 2024")
    st.subheader("Bid Amounts by Team")

    # Define the total budget for each team
    total_budget = 10000  # 110 crores, assuming this is the total budget available

    # Add a refresh button to reload the data from the CSV
    if st.button("Refresh Data"):
        st.session_state.players_bids_df = pd.read_csv('final_team.csv')

    # Get the list of unique teams from the bid data
    teams = st.session_state.players_bids_df['Franchise'].unique()

    # Dropdown to select a team
    selected_team = st.selectbox("Select a Team", teams)

    # Filter players by selected team
    team_players = st.session_state.players_bids_df[st.session_state.players_bids_df['Franchise'] == selected_team]
    
    # Add serial numbers for each player within the selected team
    team_players['No.'] = range(1, len(team_players) + 1)

    # Display team name and player bids with updated serial number
    st.subheader(f"Team: {selected_team}")
    st.dataframe(team_players[['No.', 'Player Name', 'Role','Points']])


    # Calculate the average overall rating (Ovr), assuming "Points" is the overall rating
    average_ovr = team_players['Points'].mean() if not team_players['Points'].isnull().all() else 0

    st.write(f"Average Ovr: {average_ovr:.2f}")

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
