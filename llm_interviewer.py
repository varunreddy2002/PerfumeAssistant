from openai import OpenAI
import os

def get_followup_questions(user_input: dict) -> list:
    system_prompt = (
        "You are a fragrance advisor. Based on a user's scent preferences, generate 2–3 thoughtful follow-up questions "
        "to better understand their ideal perfume. Don't repeat known inputs. Ask only what’s relevant."
    )

    prompt = f"""
    Gender: {user_input['gender']}
    Preferred Notes: {', '.join(user_input['preferred_notes'])}
    Preferred Accords: {', '.join(user_input['preferred_accords'])}
    Description: {user_input['free_text']}
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    followup = response.choices[0].message.content.strip()
    return followup.split("\n")
