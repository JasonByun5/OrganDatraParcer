import re

file_path = "ranked-claude/ranked_kidney0_all_shuffle0_trial0.out"

def find_and_extract_rankings(file_path):
    """Find the first instance of :\n\n followed by int,int pairs and extract all of them."""
    with open(file_path, "r") as file:
        content = file.read()
    
    # Normalize newlines to prevent issues with Windows/Mac files
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    
    # Search for :\n\n followed by multiple int,int pairs
    match = re.search(r":\\n\\n((?:\d+,\s*\d+\\n?)+)", content)
    if match:
        extracted_text = match.group(1).strip()  # Extract all ranking pairs
        print("extracted text: ", extracted_text)
        
        # Separate into two lists
        patients = []
        rankings = []
        
        for line in extracted_text.split("\\n"):
            line = line.strip()  # Remove leading/trailing whitespace
            print("line", line)
            parts = line.split(",")  # Split by comma
            print("parts: ", parts)
            
            # Ensure the split resulted in exactly two parts
            if len(parts) == 2:
                try:
                    patient = int(parts[0].strip())  # Convert first number
                    rank = int(parts[1].strip())  # Convert second number
                    
                    patients.append(patient)
                    rankings.append(rank)
                except ValueError:
                    print(f"Skipping invalid line: {repr(line)}")  # Debugging message
        
        print("Patients:", patients)
        print("Rankings:", rankings)
        return patients, rankings
    
    else:
        print("No matching pattern found.")
        return [], []

# Execute function
find_and_extract_rankings(file_path)
