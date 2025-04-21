import re
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("organtestingdata-d7cb159a6995.json", scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
# things above activate the google spread sheet stuff


# creates a new sheet
sheet = client.open("TestSpreadsheet").sheet1

currShuffle = 0

currTrial = 0

for currTrial in range(5):
    with open (f'ranked_kidney0_all_shuffle{currShuffle}_trial{currTrial}.out', 'r') as f:

        for lime in f:
            lime = lime.strip()
            if ("Here's the ranking" in lime) or ("I'll rank the 15 candidates based" in lime) or ("rankings" in lime):
                print(lime)
                print("Match found")
                break
            
        line = f.readline().strip() #used to get the null string
        
        patients = []
        ranks = [] # when sorting the patients list, what you change in the patient list, change in the rank list
        for i in range(15):
            line = f.readline().strip()
            
            
            temp = line.split(",")
            
            patients.append(temp[0])
            ranks.append(temp[1].strip())

        #makes the lists into ints
        patients = list(map(int, patients))  
        ranks = list(map(int, ranks))   
        
        #sorts the lists together
        sorted_patients, sorted_ranks = zip(*sorted(zip(patients, ranks)))
        sorted_ranks = list(sorted_ranks)
        
        cells = []
        for i, r, in enumerate(sorted_ranks, start=3):
            cell = sheet.cell(i, 3 + currTrial)
            cell.value = r
            cells.append(cell)
        
        #puts the things into the spread sheet
        sheet.update_cells(cells)
            
