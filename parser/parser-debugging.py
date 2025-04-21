import csv
import re
import os


def extract_rankings_gemini(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    content = content.replace("\\n", "\n")

    match = re.search(r"\n((?:\d+,\s*\d+\s*\n?)+)", content)

    if match:
        extracted_text = match.group(1).strip()

        patients = []
        rankings = []
        
        for line in extracted_text.split("\n"):
            line = line.strip()
            parts = line.split(",")
            
            if len(parts) == 2:
                try:
                    patient = int(parts[0].strip()) 
                    rank = int(parts[1].strip())
                    
                    patients.append(patient)
                    rankings.append(rank)
                except ValueError:
                    print(f"Skipping invalid line: {repr(line)}")
        
        print ("Presorted patients: ", patients)
        print ("Presorted rankings: ", rankings)
        
        sorted_patients, sorted_rankings = zip(*sorted(zip(patients, rankings)))
        min_patient = sorted_patients[0]
        max_patient = sorted_patients[-1]
        
        full_patients = list(range(min_patient, max_patient + 1))
        full_rankings = [None] * (max_patient - min_patient + 1)
        
        for patient, rank in zip(sorted_patients, sorted_rankings):
            full_rankings[patient - min_patient] = rank
        
        return full_patients, full_rankings
    
    else:
        print(f"No matching, kidney {currKidney} ,shuffle {currShuffle}, trial {currTrial}")
        return [], []


model = "gemini"
types = "all"
currKidney = 0
currShuffle = 0
currTrial = 1
extract_function = extract_rankings_gemini

#for currKidney in range(2):
    
#for currShuffle in range(3): 
        
#for currTrial in range(5):

file_path = f"results/{model}/ranked/ranked_kidney{currKidney}_{types}_shuffle{currShuffle}_trial{currTrial}.out"
patients, rankings = extract_function(file_path)

print(f"       Trial: {currTrial}")
print ("          patients: ", patients)
print ("          rankings: ", rankings)
print(f"    Shuffle: {currShuffle}")
print(f"Kidney: {currKidney}")
