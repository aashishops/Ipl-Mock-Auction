import csv

# Data for franchises, retained players, and bid amounts (RTM option removed)
data = [
    ["Mumbai Indians", "Jasprit Bumrah", 18],
    ["Mumbai Indians", "Suryakumar Yadav", 16.35],
    ["Mumbai Indians", "Hardik Pandya", 16.35],
    ["Mumbai Indians", "Rohit Sharma", 16.30],
    ["Mumbai Indians", "Tilak Varma", 8],
    ["Kolkata Knight Riders", "Rinku Singh", 13],
    ["Kolkata Knight Riders", "Varun Chakaravarthy", 12],
    ["Kolkata Knight Riders", "Sunil Narine", 12],
    ["Kolkata Knight Riders", "Andre Russell", 12],
    ["Kolkata Knight Riders", "Harshit Rana", 4],
    ["Kolkata Knight Riders", "Ramandeep Singh", 4],
    ["Chennai Super Kings", "Ruturaj Gaikwad", 18],
    ["Chennai Super Kings", "Matheesha Pathirana", 13],
    ["Chennai Super Kings", "Shivam Dube", 12],
    ["Chennai Super Kings", "Ravindra Jadeja", 18],
    ["Chennai Super Kings", "MS Dhoni", 4],
    ["Rajasthan Royals", "Sanju Samson", 18],
    ["Rajasthan Royals", "Yashasvi Jaiswal", 18],
    ["Rajasthan Royals", "Riyan Parag", 14],
    ["Rajasthan Royals", "Dhruv Jurel", 14],
    ["Rajasthan Royals", "Shimron Hetmyer", 11],
    ["Rajasthan Royals", "Sandeep Sharma", 4],
    ["Royal Challengers Bengaluru", "Virat Kohli", 21],
    ["Royal Challengers Bengaluru", "Rajat Patidar", 11],
    ["Royal Challengers Bengaluru", "Yash Dayal", 5],
    ["Delhi Capitals", "Axar Patel", 16.50],
    ["Delhi Capitals", "Kuldeep Yadav", 13.25],
    ["Delhi Capitals", "Tristan Stubbs", 10],
    ["Delhi Capitals", "Abishek Porel", 4],
    ["Gujarat Titans", "Rashid Khan", 18],
    ["Gujarat Titans", "Shubman Gill", 16.50],
    ["Gujarat Titans", "Sai Sudharsan", 8.50],
    ["Gujarat Titans", "Rahul Tewatia", 4],
    ["Gujarat Titans", "Shahrukh Khan", 4],
    ["Lucknow Super Giants", "Nicholas Pooran", 21],
    ["Lucknow Super Giants", "Ravi Bishnoi", 11],
    ["Lucknow Super Giants", "Mayank Yadav", 11],
    ["Lucknow Super Giants", "Mohsin Khan", 4],
    ["Lucknow Super Giants", "Ayush Badoni", 4],
    ["Punjab Kings", "Shashank Singh", 5.5],
    ["Punjab Kings", "Prabhsimran Singh", 4],
    ["Sunrisers Hyderabad", "Heinrich Klaasen", 23],
    ["Sunrisers Hyderabad", "Pat Cummins", 18],
    ["Sunrisers Hyderabad", "Abhishek Sharma", 14],
    ["Sunrisers Hyderabad", "Travis Head", 14],
    ["Sunrisers Hyderabad", "Nitish Kumar Reddy", 6]
]

# Column names
fields = ["franchise", "player name", "bid amount"]

# File path
file_path = "code\ipl_franchise_players.csv"

# Writing to CSV
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing the header
    writer.writerow(fields)
    # Writing the data
    writer.writerows(data)

print(f"Data has been written to {file_path}")
