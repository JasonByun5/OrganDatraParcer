import csv
import re
import os

def extract_rankings_claude(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    
    #\\n\\n
    match = re.search(r"((?:\d+,\s*\d+\\n?)+)", content)
    if match:
        extracted_text = match.group(1).strip()

        patients = []
        rankings = []
        
        for line in extracted_text.split("\\n"):
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
        
        sorted_patients, sorted_rankings = zip(*sorted(zip(patients, rankings)))
        min_patient = sorted_patients[0]
        max_patient = sorted_patients[-1]
        
        full_patients = list(range(min_patient, max_patient + 1))
        full_rankings = [None] * (max_patient - min_patient + 1)
        
        for patient, rank in zip(sorted_patients, sorted_rankings):
            full_rankings[patient - min_patient] = rank
        
        return full_patients, full_rankings
        
    else:
        print(f"      No matching, kidney {currKidney} ,shuffle {currShuffle}, trial {currTrial}")
        return [], []


def extract_rankings_gpt_alt(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    content = content.replace("\\n", "\n")
    
    pattern = r"\d+\.\s*Candidate\s+(?:ID(?::)?\s+)?(\d+),\s*(?:Ranking(?::)?\s*)?(\d+)"
    matches = re.findall(pattern, content)
    
    
    if matches:

        patients = [int(candidate) for candidate, rank in matches]
        rankings = [int(rank) for candidate, rank in matches]
        
        sorted_patients, sorted_rankings = zip(*sorted(zip(patients, rankings)))
        
        min_patient = min(sorted_patients)
        max_patient = max(sorted_patients)
        
        full_patients = list(range(min_patient, max_patient + 1))
        full_rankings = [None] * (max_patient - min_patient + 1)
        
        for patient, rank in zip(sorted_patients, sorted_rankings):
            full_rankings[patient - min_patient] = rank
        
        return full_patients, full_rankings
    
    else:
        return [], []

def extract_rankings_gpt_alt2(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    content = content.replace("\\n", "\n")

    pattern = r"\n\n(?:```(?:plaintext)?)?[\n\r]*((?:(?:\d+\.\s*)?\s*(\d+),\s*(\d+)\s*\n?)+)"
    match = re.search(pattern, content)
    
    if match:
        extracted_text = match.group(1).strip()

        patients = []
        rankings = []
        
        for line in extracted_text.split("\n"):
            line = line.strip()
            parts = re.split(r"[ ,]+", line)
            if len(parts) >= 2:
                try:
                    patient = int(parts[-2].strip()) 
                    rank = int(parts[-1].strip())
                    
                    patients.append(patient)
                    rankings.append(rank)
                except ValueError:
                    print(f"Skipping invalid line: {repr(line)}")
        
        
        sorted_patients, sorted_rankings = zip(*sorted(zip(patients, rankings)))
        min_patient = sorted_patients[0]
        max_patient = sorted_patients[-1]
        
        full_patients = list(range(min_patient, max_patient + 1))
        full_rankings = [None] * (max_patient - min_patient + 1)
        
        for patient, rank in zip(sorted_patients, sorted_rankings):
            full_rankings[patient - min_patient] = rank
        
        return full_patients, full_rankings
    
    else:
        print(f"      No matching, kidney {currKidney} ,shuffle {currShuffle}, trial {currTrial}")
        return [], []

def extract_rankings_gpt(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    content = content.replace("\\n", "\n")

    pattern = r"\n((?:\d+,\s*\d+\s*\n?)+)"
    match = re.search(pattern, content)
    
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
        
        
        sorted_patients, sorted_rankings = zip(*sorted(zip(patients, rankings)))
        min_patient = sorted_patients[0]
        max_patient = sorted_patients[-1]
        
        full_patients = list(range(min_patient, max_patient + 1))
        full_rankings = [None] * (max_patient - min_patient + 1)
        
        for patient, rank in zip(sorted_patients, sorted_rankings):
            full_rankings[patient - min_patient] = rank
        
        return full_patients, full_rankings
    
    else:
        return [], []



models = {
    "claude":{
        "types": ["all", "demo_only"],
        "endingType": ["all", "demo"],
        "folderType": ["claude-all", "claude-demo"],
        "extract_function" : extract_rankings_claude,
    },
    "gpt":{
        "types": ["all", "demo_only"],
        "endingType": ["all", "demo"],
        "folderType" : ["gpt-all", "gpt-demo"],
        "extract_function" : extract_rankings_gpt,
    }
}

for model, params in models.items():
    types = params["types"]
    folderType = params["folderType"]
    extract_function = params["extract_function"]
    endingType = params["endingType"]

    for i in range(len(types)):

        for currKidney in range(20):
            
            compiled_rankings = {}
            
            for currShuffle in range(3):       
                for currTrial in range(5):
                    file_path = f"results/{model}/ranked/ranked_kidney{currKidney}_{types[i]}_shuffle{currShuffle}_trial{currTrial}.out"
                    patients, rankings = extract_function(file_path)
                    
                    if model == "gpt" and patients == []:
                        patients, rankings = extract_rankings_gpt_alt(file_path)
                        
                    if model == "gpt" and patients == []:
                        patients, rankings = extract_rankings_gpt_alt2(file_path)

                    for idx, (patient, rank) in enumerate(zip(patients, rankings)):
                            if patient not in compiled_rankings:
                                compiled_rankings[patient] = [None] * 15
                            
                            # Map shuffle-trial to correct column index
                            col_index = 5 * currShuffle + currTrial  
                            compiled_rankings[patient][col_index] = rank
                    
            file_path_created = f"parcerResults/{folderType[i]}/{model}_ranked_borda_kidney{currKidney}_{endingType[i]}.csv"       
            with open(file_path_created, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Candidate","Shuffle0_Trial0","Shuffle0_Trial1","Shuffle0_Trial2","Shuffle0_Trial3","Shuffle0_Trial4",
                                "Shuffle1_Trial0","Shuffle1_Trial1","Shuffle1_Trial2","Shuffle1_Trial3","Shuffle1_Trial4",
                                "Shuffle2_Trial0","Shuffle2_Trial1","Shuffle2_Trial2","Shuffle2_Trial3","Shuffle2_Trial4"])
                
                for candidate, ranking_list in sorted(compiled_rankings.items()):
                    writer.writerow([candidate] + ranking_list)
                            
            print(f'Kidney {currKidney} updated')

        print(f'Type: {types[i]} updated')
        
    print(f'Model: {model} updated')
    print('------------------------------------')
    print()
