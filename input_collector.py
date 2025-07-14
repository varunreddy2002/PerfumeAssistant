# input_collector.py

def collect_user_input():
    print("\nPersonalized Scent Recommender - User Input\n")

    gender = input("Preferred gender profile for the scent (feminine, masculine, unisex): ").strip().lower()

    print("\nEnter 2–3 specific scent notes you prefer (e.g., vanilla, rose, citrus):")
    notes_raw = input("Separate each with a comma: ")
    preferred_notes = [n.strip().lower() for n in notes_raw.split(",")]

    print("\nEnter 2–3 general scent styles or accords you prefer (e.g., floral, woody, sweet):")
    accords_raw = input("Separate each with a comma: ")
    preferred_accords = [a.strip().lower() for a in accords_raw.split(",")]

    free_text = input("\nOptional: Describe what you're looking for in your own words (or leave blank): ")

    return {
        "gender": gender,
        "preferred_notes": preferred_notes,
        "preferred_accords": preferred_accords,
        "free_text": free_text
    }

# Only runs if you execute this file directly from terminal
if __name__ == "__main__":
    user_data = collect_user_input()
    
    print("\n✅ Collected User Input:")
    print(user_data)

import os
import json

user_input_file = "user_input.json"

# Load existing data if it's a valid list
if os.path.exists(user_input_file):
    with open(user_input_file, "r") as f:
        try:
            all_inputs = json.load(f)
            if not isinstance(all_inputs, list):
                all_inputs = []
        except json.JSONDecodeError:
            all_inputs = []
else:
    all_inputs = []

# Append new input
all_inputs.append(user_data)

# Save back to file
with open(user_input_file, "w") as f:
    json.dump(all_inputs, f, indent=4)
    print("\n📁 Appended to user_input.json")


