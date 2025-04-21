import openai
#import os

#api_key = os.getenv("API_KEY")
openai_client = openai.Client(api_key="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")  # Create an OpenAI client

# Read the file content
file_path = "ranked_kidney0_all_shuffle0_trial2.out"  # Adjust this path as needed

try:
    with open(file_path, "r") as file:
        text_data = file.read()
except FileNotFoundError:
    print("Error: File not found.")
    text_data = ""

# Only call OpenAI API if there is valid data
if text_data:
    messages = [
        {"role": "user", "content": f"If I was to give you this file {text_data}, past line 80 there are the rankings that I need you to parse. The first value in the line is the patient as the second value is the ranking. Output ONLY the 2 arrays and do not give labels to them"}
    ]

    response = openai_client.chat.completions.create(  # Updated method call
        model="gpt-4o-mini",
        messages=messages
    )

    print(response.choices[0].message.content)  # Updated response format
else:
    print("No data found in the file.")