import streamlit as st
import pandas as pd

# Load the auction and bid data CSV files (only once per session)
@st.cache_data
def load_data():
    auction_df = pd.read_csv('mock_auction_players.csv')
    players_bids_df = pd.read_csv('players_bids.csv')
    return auction_df, players_bids_df

# Public page
def public_page():
    st.title("IPL Auction 2024")
    st.subheader("Bid Amounts by Team")

    # Define the total budget for each team
    total_budget = 10000  # 110 crores, assuming this is the total budget available

    # Add a refresh button to reload the data from the CSV
    if st.button("Refresh Data"):
        st.session_state.players_bids_df = pd.read_csv('players_bids.csv')

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
    st.dataframe(team_players[['No.', 'Player Name', 'Role', 'Bid Amount', 'Points']])

    # Calculate the sum of the bid amounts for the current team
    total_bid_amount = team_players['Bid Amount'].sum()

    # Calculate the remaining budget
    remaining_budget = total_budget - total_bid_amount

    # Calculate the average overall rating (Ovr), assuming "Points" is the overall rating
    average_ovr = team_players['Points'].mean() if not team_players['Points'].isnull().all() else 0

    # Display the remaining budget and average Ovr
    st.write(f"Remaining Budget: ₹{(remaining_budget/100):.2f} Crores")
   # st.write(f"Average Ovr: {average_ovr:.2f}")

        # Add a clickable link at the bottom left
    st.markdown(
        """
        <div style="position: fixed; bottom: 50px; left: 10px;">
            <a href="http://192.168.0.101:4201/" target="_blank" style="text-decoration: none; color: #007BFF;">
                Go to Secret Ballot Page
            </a>
        </div>
        <div style="position: fixed; bottom: 10px; left: 10px;">
            <a href="http://192.168.0.101:4209/" target="_blank" style="text-decoration: none; color: #007BFF;">
                Go to Team Submisson Page
            </a>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.download_button(
        label= "Download Players List",
        data = open(r"C:\Users\thush\OneDrive\Desktop\MOCK AUCTION 2024 DEC\Ipl-Mock-Auction\mock_auction_players.csv")
.read(),
        file_name = "mock_auction_player.csv",
        mime = "text/csv",
    )

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
    
