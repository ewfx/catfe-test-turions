from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from src.app.service.bddtestgeneratorservice import BDDTestGeneratorService

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Angular frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the service
generator_service = BDDTestGeneratorService()

class RequestData(BaseModel):
    context: str
# MongoDB Connection
client = MongoClient("mongodb+srv://bddtestuser:bddtestuser@cluster0.imorp.mongodb.net/BDDTESTMAPPER?retryWrites=true&w=majority")
db = client["TestTurions"]
collection = db["BDDTESTMAPPER"]

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

@app.post("/generate-openai-ol")
def generate_test_cases_with_ol_openai(request_data: RequestData):
    try:
        # Extract context from the request
        context = request_data.context

        if not context:
            raise HTTPException(status_code=400, detail="Context is required")

        # Generate test cases using the service
        response = generator_service.generate_test_cases_openrouter(context)

        # Return the generated test cases as a JSON response
        return {"test_cases": response}
    except Exception as e:
        # Handle errors and return a meaningful response
        raise HTTPException(status_code=500, detail=str(e))
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

@app.get("/features/", response_model=List[Feature])
def get_all_features():
    try:
        features = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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