from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_service.bdd_generator import generate_bdd_scenario

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate_bdd/")
async def generate_bdd(prompt_request: PromptRequest):
    try:
        bdd_scenario = generate_bdd_scenario(prompt_request.prompt)
        return {"scenario": bdd_scenario}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
