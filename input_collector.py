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

# Example usage
if __name__ == "__main__":
    user_input = collect_user_input()
    print("\nCollected User Input:")
    print(user_input)
