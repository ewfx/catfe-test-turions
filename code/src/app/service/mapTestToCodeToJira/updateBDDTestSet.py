from pymongo import MongoClient

def connect_to_mongodb():
    # MongoDB connection string
    connection_string = "mongodb+srv://bddtestuser:bddtestuser@cluster0.imorp.mongodb.net/BDDTESTMAPPER?retryWrites=true&w=majority"
    
    try:
        # Create a MongoDB client
        client = MongoClient(connection_string)
        
        # Access the database
        db = client["TestTurions"]
        
        # Test the connection by listing collections
        collections = db.list_collection_names()
        print("Connected to MongoDB!")
        #print("Collections in the database:", collections)
        
        return db
    except Exception as e:
        print("Failed to connect to MongoDB:", str(e))
        return None

def search_field_in_collection(db, collection_name, field_value):
    try:
        # Access the collection from the database
        collection = db[collection_name]
        print(f"Accessing collection: {collection_name}")
        
        # Define the query
        query = {"file": field_value}
        #print(f"Query: {query}")
        
        # Execute the query
        results = collection.find(query)
        print(f"Documents matching '{field_value}' in collection '{collection_name}':")
        
        # Convert results to a list
        documents = list(results)
        print(documents)
        
        if not documents:
            print("No documents found.")
        
        # Print each document and extract the feature_id
        for document in documents:
            #print(document)
            primaryFeatureDependency = document.get("primaryFeatureDependency")
            #print(feature_id)
            if primaryFeatureDependency:
                print(f"primaryFeatureDependency: {primaryFeatureDependency}")
                
                
        
        return documents
    except Exception as e:
        print(f"Failed to search in collection '{collection_name}':", str(e))
        return []
def search_and_update_scenarios_by_state(db, collection_name, featureName, state,jira):
    try:
        # Access the collection
        print(f"Accessing collection: {collection_name}")
        collection = db[collection_name]
        
        # Search for the feature_id in the collection
        print(featureName)
        query = {"featureName": featureName}
        results = collection.find(query)
        #print(results)
        
        # Update the state in the BDDTESTMAPPER database
# Update the state in the BDDTESTMAPPER database
        jira_with_changes = f"Changes for {jira}" 
        update_query = {"featureName": featureName}  # Ensure this matches the document structure
        update_data = {"$set": {"state": state, "suggestedAIContextChange": jira_with_changes}}
        #print(f"Update Query: {update_query}")
        #print(f"Update Data: {update_data}")
        
        # Perform the update
        update_result = collection.update_one(update_query, update_data)
        print(f"Matched Count: {update_result.matched_count}")
        print(f"Modified Count: {update_result.modified_count}")
        
        if update_result.matched_count > 0:
            print(f"Updated state for featureName: {featureName}")
        else:
            print(f"No matching document found for featureName: {featureName}")
        
    except Exception as e:
        print(f"Failed to search in collection '{collection_name}':", str(e))

if __name__ == "__main__":
    # Connect to MongoDB
    db = connect_to_mongodb()
    #print(db)
    

                    