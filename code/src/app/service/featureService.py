from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

app = FastAPI()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["bddDatabase"]
collection = db["features"]

class Scenario(BaseModel):
    scenarioId: str
    scenarioName: str
    scenarioDescription: str
    given: str
    when: str
    then: str

class Feature(BaseModel):
    featureId: str
    featureName: str
    shortDescription: str
    featureContext: str
    suggestedAIContextChange: str
    state: str
    testScenarios: List[Scenario] = []

@app.post("/features/")
def create_feature(feature: Feature):
    feature_dict = feature.dict()
    collection.insert_one(feature_dict)
    return {"message": "Feature created successfully"}

@app.get("/features/{featureId}")
def get_feature(featureId: str):
    feature = collection.find_one({"featureId": featureId})
    if feature:
        feature["_id"] = str(feature["_id"])  # Convert ObjectId to string
        return feature
    raise HTTPException(status_code=404, detail="Feature not found")

@app.put("/features/{featureId}")
def update_feature(featureId: str, feature: Feature):
    updated = collection.update_one({"featureId": featureId}, {"$set": feature.dict()})
    if updated.modified_count:
        return {"message": "Feature updated successfully"}
    raise HTTPException(status_code=404, detail="Feature not found")

@app.delete("/features/{featureId}")
def delete_feature(featureId: str):
    deleted = collection.delete_one({"featureId": featureId})
    if deleted.deleted_count:
        return {"message": "Feature deleted successfully"}
    raise HTTPException(status_code=404, detail="Feature not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
