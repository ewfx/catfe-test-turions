from flask import Flask, request, jsonify
from src.app.service.bddtestgeneratorservice import BDDTestGeneratorService

# Initialize Flask app
app = Flask(__name__)

# Initialize the service with the model path
# model_path = "C:/Users/abina/OneDrive/Documents/GitHub/catfe-test-turions/code/src/models/gpt2_model"
generator_service = BDDTestGeneratorService()

# @app.route('/generate', methods=['POST'])
# def generate_test_cases():
#     try:
#         # Parse the input JSON request
#         data = request.json
#         context = data.get("context")
#         if not context:
#             return jsonify({"error": "Context is required"}), 400
        
#         # Call the service to generate BDD test cases
#         generated_test_cases = generator_service.generate_test_cases(context)
        
#         # Return the generated output
#         return jsonify({"test_cases": generated_test_cases})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route("/generate-openai-ol", methods=["POST"])
def generate_test_cases_with_ol_openai():
    try:
        # Parse the JSON request body
        request_data = request.get_json()
        context = request_data.get("context", "")

        if not context:
            return jsonify({"error": "Context is required"}), 400

        # Generate test cases using the service
        response = generator_service.generate_test_cases_openrouter(context)

        # Return the generated test cases as a JSON response
        return jsonify({"test_cases": response}), 200
    except Exception as e:
        # Handle errors and return a meaningful response
        return jsonify({"error": str(e)}), 500

# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)