import openai
import torch
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer

class BDDTestGeneratorService:
    # def __init__(self, model_path):
    #     # Initialize and load the model and tokenizer with local files
    #     self.model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)
    #     self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    #     self.model.eval()
    # def generate_test_cases(self, context):

    #     scenario = "A user withdraws money from an ATM"
    #     test_data = "Account Balance: 1000\nWithdrawal Amount: 500\nATM Withdrawal Limit: 1000\n"

    #     prompt= f"""Write test cases in proper Gherkin BDD format with GIven, When, Then.
    #     Only return the test cases, do not include extra explanation or link.

    #     """
        
    #     # Prepare input for the model
    #     inputs = self.tokenizer.encode(prompt, return_tensors="pt")
    #     print(F"Input IdsShape: {inputs.shape}")

    #     # Generate text
    #     with torch.no_grad():
    #         outputs = self.model.generate(
    #             inputs,
    #               max_length=400,
    #                 num_return_sequences=1,
    #                   temperature=0.3,
    #                     top_k=20, repetition_penalty=2.5,
    #                     no_repeat_ngram_size=4,
    #                     early_stopping=True,)
        
    #     print(F"Output IdsShape: {outputs.shape}")
    #     # Decode and return the generated text
    #     return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


    def __init__(self):
        # Initialize the OpenAI API key
        self.api_key = "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"
        openai.api_key = self.api_key

    def generate_test_cases_openrouter(self, context):
        try:
            # Prepare the request to the OpenRouter API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek/deepseek-r1-zero:free",  # Replace with the correct model ID
                "prompt": f"Just provide BDD test cases based on this context without any extra text :\n\n{context}",
                "temperature": 0.8,  # Increase for creativity
                "max_tokens": 200,   # Limit the response length
                "top_p": 1.0,        # Control diversity
                "n": 1               # Generate a single response
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                # Extract and return the generated test cases
                return response.json()["choices"][0]["text"].strip()
            else:
                raise ValueError(f"Failed to generate test cases: {response.text}")
        except Exception as e:
            # Log or handle errors appropriately
            raise ValueError(f"Failed to generate test cases: {str(e)}")