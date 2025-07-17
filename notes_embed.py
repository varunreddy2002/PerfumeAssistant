import google.generativeai as genai
import os
import pickle
import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

NOTE_EMBEDDINGS_PATH = "note_embeddings.pkl"


def get_gemini_embedding(text: str) -> list:
    return genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )["embedding"]


def extract_notes(col):
    return [n.strip().lower() for n in str(col).split(",") if n.strip()]


def build_and_save_embeddings(csv_path: str):
    df = pd.read_csv(csv_path)
    note_set = set()
    for col in ['Top', 'Middle', 'Base']:
        for row in df[col]:
            note_set.update(extract_notes(row))

    note_list = sorted(note_set)
    note_embeddings = {note: get_gemini_embedding(note) for note in note_list}

    with open(NOTE_EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(note_embeddings, f)

    print(f"✅ Saved {len(note_embeddings)} note embeddings to {NOTE_EMBEDDINGS_PATH}")


def load_embeddings() -> dict:
    if not os.path.exists(NOTE_EMBEDDINGS_PATH):
        raise FileNotFoundError("❌ Embeddings file not found. Run build_and_save_embeddings() first.")
    with open(NOTE_EMBEDDINGS_PATH, "rb") as f:
        return pickle.load(f)


def find_closest_note(input_note: str, known_embeddings: dict) -> str:
    input_vec = get_gemini_embedding(input_note)
    max_score = -1
    best_note = None
    for note, vec in known_embeddings.items():
        score = cosine_similarity([input_vec], [vec])[0][0]
        if score > max_score:
            max_score = score
            best_note = note
    return best_note


if __name__ == "__main__":
    build_and_save_embeddings("perfume_list.csv")
