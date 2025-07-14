from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    gender: str
    occasion: str
    scent_pref: str
    rating: float = None
    country: str = None

@app.get("/")
def read_root():
    return {"message": "Perfume Assistant API is running"}

@app.post("/collect-input")
def handle_user_input(user_input: UserInput):
    # You can add logic here to process or forward the input later
    return {"collected_input": user_input.dict()}
