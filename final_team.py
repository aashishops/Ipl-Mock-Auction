import streamlit as st
import pandas as pd
import os

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
print("lol")
print(players_df)
# Streamlit UI
st.title("IPL Admin Portal")

# Team Admin Login Section
st.subheader("Admin Login")

# Dropdown for Team Selection
team_name = st.selectbox("Select IPL Team", list(team_credentials.keys()))
password = st.text_input("Enter Password", type="password")

# Function to validate credentials
def validate_credentials(team_name, password):
    return team_credentials.get(team_name) == password

# Login button
if st.button("Login"):
    if validate_credentials(team_name, password):
        st.success(f"Welcome, {team_name}! You are successfully logged in.")

        # Filter players based on the franchise (team)
        team_players = players_df[players_df['Franchise'] == team_name].copy()

        st.subheader("Select Your Starting 11")

        # Initialize session state for player selection (if not already initialized)
        if 'selected_players' not in st.session_state:
            st.session_state.selected_players = [None] * 11

        with st.form(key="team_selection_form"):
            remaining_players = team_players['Player Name'].tolist()

            for i in range(11):
                player_options = [
                    player for player in remaining_players 
                    if player not in st.session_state.selected_players
                ]

                # Display dropdown only if options are available
                if player_options:
                    selected_player = st.selectbox(
                        f"Select Player {i + 1}", 
                        options=["Select a player"] + player_options, 
                        key=f"player_{i}"
                    )
                    if selected_player != "Select a player":
                        st.session_state.selected_players[i] = selected_player
                        remaining_players.remove(selected_player)
                else:
                    st.warning(f"No more players available for slot {i + 1}.")
                    break

            # Submit button for the form
            submit_button = st.form_submit_button("Submit Team")

        if submit_button:
            st.write("Submit button clicked")  # Debug statement
            print("submitted")
            # Filter None values and ensure 11 players are selected
            selected_players_set = list(filter(None, st.session_state.selected_players))
            st.write(f"Selected players: {selected_players_set}")  # Debug statement
            if len(selected_players_set) != 11:
                st.error("You must select exactly 11 unique players!")
            else:
                # Retrieve player details for the selected players
                selected_team_df = team_players[team_players['Player Name'].isin(selected_players_set)]
                selected_team_df = selected_team_df[['Player Name', 'Franchise', 'Points', 'Role']]
                st.write(f"Selected team dataframe: {selected_team_df}")  # Debug statement

                # Define CSV file path
                csv_file = 'final_team.csv'
                st.write(f"CSV file path: {csv_file}")  # Debug statement

                # Append data to the CSV file
                if os.path.exists(csv_file):
                    selected_team_df.to_csv(csv_file, mode='a', header=False, index=False)
                else:
                    selected_team_df.to_csv(csv_file, mode='w', header=True, index=False)

                # Success message
                st.success("Team submitted successfully!")

                # Calculate and display budget and points information
                total_budget = 100  # Example total budget
                total_spent = selected_team_df['Points'].sum()
                remaining_budget = total_budget - total_spent
                average_points = selected_team_df['Points'].mean()

                st.write("Selected Team:")
                st.dataframe(selected_team_df)

                st.write(f"Total Budget: {total_budget}")
                st.write(f"Remaining Budget: {remaining_budget}")
                st.write(f"Average Points of Selected Team: {average_points:.2f}")

                # Reset selections for the next submission
                st.session_state.selected_players = [None] * 11
    else:
        st.error("Invalid username or password. Please try again.")