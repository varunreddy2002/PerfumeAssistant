# input_collector.py
import os
import json

def collect_user_input():
    print("\nPersonalized Scent Recommender - User Input\n")

    user = input("Username: ").strip().lower()

    gender = input("Preferred gender profile for the scent (feminine, masculine, unisex): ").strip().lower()

    a = 0
    while(a==0):
        print("\nEnter the user's age:")
        a1 = input("Strictly write the answer as a number:")
        try:
            age = int(a1)
            a = 1
        except:
            print("The given response was not in the correct type, please give a new response.")

    country = input("What is the preferred perfume country of production: ").strip().lower()

    brand = input("Perfume Brand preference: ").strip().lower()

    print("\nEnter 2–3 specific scent notes you prefer (e.g., vanilla, rose, citrus):")
    notes_raw = input("Separate each with a comma: ")
    preferred_notes = [n.strip().lower() for n in notes_raw.split(",")]

    print("\nEnter 2–3 general scent styles or accords you prefer (e.g., floral, woody, sweet):")
    accords_raw = input("Separate each with a comma: ")
    preferred_accords = [a.strip().lower() for a in accords_raw.split(",")]

    t= 0
    while(t==0):
        print("\nEnter the expected temperature for the day:")
        temperature = input("Strictly write the answer as a number, in fahrenheit:")
        try:
            temp = int(temperature)
            t = 1
        except:
            print("The given response was not in the correct type, please give a new response.")
    
    mood = input("\nWhat mood do you want to evoke (e.g., bold, sincere, emo, romantic): ")

    occasion = input("\nWhat occasion is the perfume for:")

    humidity = input("Level of expected humidity (high, medium, low, none): ").strip().lower()

    free_text = input("\nList any futher descriptions/parameters for the perfume: ")

    return {
        "user":user,
        "gender": gender,
        "age":age,
        "country":country,
        "brand":brand,
        "preferred_notes": preferred_notes,
        "preferred_accords": preferred_accords,
        "temperature":temp,
        "mood":mood,
        'occasion':occasion,
        'humidity':humidity,
        "free_text": free_text
    }

def json_append(user_data):
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

    all_inputs.append(user_data)

    # Save back to file
    with open(user_input_file, "w") as f:
        json.dump(all_inputs, f, indent=4)
        print("\n📁 Appended to user_input.json")

# Only runs if you execute this file directly from terminal
# if __name__ == "__main__":
#     user_data = collect_user_input()
    
#     print("\n✅ Collected User Input:")
#     print(user_data)

# user_input_file = "user_input.json"

# # Load existing data if it's a valid list
# if os.path.exists(user_input_file):
#     with open(user_input_file, "r") as f:
#         try:
#             all_inputs = json.load(f)
#             if not isinstance(all_inputs, list):
#                 all_inputs = []
#         except json.JSONDecodeError:
#             all_inputs = []
# else:
#     all_inputs = []

# all_inputs.append(user_data)

# # Save back to file
# with open(user_input_file, "w") as f:
#     json.dump(all_inputs, f, indent=4)
#     print("\n📁 Appended to user_input.json")


