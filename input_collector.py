# input_collector.py
import os
import json

def collect_user_input():
    
    prompt = input("Explain in detail what type of perfume/cologne you would like to find:")

    return {
        "prompt":prompt
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


