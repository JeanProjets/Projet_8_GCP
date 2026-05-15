import requests
import urllib.parse
import pandas as pd

# 1. Define your base API URL
base_url = "https://predictionsentiments-azepf7eme8dvftaa.francecentral-01.azurewebsites.net/feeling_predictions/"
# URL locale pour MLFlow
#base_url = "http://127.0.0.1:8000/feeling_predictions/"

# 2. Define a list of 10 different sentences (mixing happy and sad to test your model)
sentences = [
    "I just got a promotion at work and I am thrilled!",
    "My dog passed away yesterday and my heart is broken.",
    "The weather is absolutely beautiful today, I love it.",
    "I failed my math exam despite studying all night.",
    "We had a wonderful family dinner with lots of laughs.",
    "I feel so lonely and isolated in this new city.",
    "Winning the championship was the best moment of my life.",
    "My flight got canceled and I missed my best friend's wedding.",
    "I am enjoying a nice, relaxing cup of coffee by the window.",
    "Everything is going wrong today and I just want to cry."
]

# 3. Initialize an empty list to store all the results
all_results = []

headers = {"accept": "application/json"}

print("Starting predictions...\n")

# 4. Loop through each sentence in the list
for text in sentences:
    # URL-encode the sentence safely
    encoded_text = urllib.parse.quote(text)
    full_url = f"{base_url}{encoded_text}"
    
    try:
        # Call the API
        response = requests.get(full_url, headers=headers)
        response.raise_for_status() # Check for HTTP errors like 500 or 404
        
        # Parse the JSON response {"text": "...", "feeling_result": "..."}
        api_data = response.json()
        
        # Extract the prediction
        prediction = api_data.get("feeling_result")
        
        # Store the success result in our list as a dictionary
        all_results.append({
            "sentence": text,
            "prediction": prediction,
            "status": "success"
        })
        
        print(f"Processed: '{text[:30]}...' -> {prediction.upper()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error processing '{text[:30]}...': {e}")
        
        # If there is an error, we still store it so we don't lose track
        all_results.append({
            "sentence": text,
            "prediction": "ERROR",
            "status": str(e)
        })

print("\n--- All 10 requests completed! ---")

# 5. Display and save the stored results
# Converting the list of dictionaries into a Pandas DataFrame is the easiest way to handle the data
df_results = pd.DataFrame(all_results)

print("\nHere is your final data table:")
print(df_results)

# Save the results to a CSV file in your folder
csv_filename = "api_predictions_results.csv"
df_results.to_csv(csv_filename, index=False, encoding="utf-8")
print(f"\nResults have been successfully saved to '{csv_filename}'.")