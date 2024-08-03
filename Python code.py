from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Define the possible choices
choices = ["snake", "water", "gun"]

# Define a request model
class Choice(BaseModel):
    user_choice: str

def determine_winner(user_choice: str, computer_choice: str) -> str:
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "snake" and computer_choice == "water") or \
         (user_choice == "water" and computer_choice == "gun") or \
         (user_choice == "gun" and computer_choice == "snake"):
        return "You win!"
    else:
        return "You lose!"

@app.post("/play")
def play_game(choice: Choice):
    user_choice = choice.user_choice.lower()
    if user_choice not in choices:
        return {"error": "Invalid choice. Please choose snake, water, or gun."}
    
    computer_choice = random.choice(choices)
    result = determine_winner(user_choice, computer_choice)
    
    return {
        "user_choice (snake/water/gun)": user_choice,
        "computer_choice": computer_choice,
        "result": result
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Snake Water Gun game! Make a POST request to /play with your choice."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.4", port=8000)
