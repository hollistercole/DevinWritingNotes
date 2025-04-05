"""
Script to query Perplexity-Sonar-Reasoning about Lea Michele's tour plans
using the PoeLocalServer with fallback to other available models if needed.
"""

import requests
import json
import sys
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = "http://0.0.0.0:8000/api/chat"

PRIMARY_MODEL = "Perplexity-Sonar-Reasoning"
FALLBACK_MODELS = ["Claude-3.5-Sonnet", "GPT-4o", "Claude-3-Opus", "Claude-3-Haiku"]

def get_available_models():
    """
    Get a list of available models from the PoeLocalServer.

    Returns:
        list: List of available model names
    """
    try:
        response = requests.get("http://0.0.0.0:8000/api/tags")
        if response.status_code == 200:
            models_data = response.json()
            available_models = [model["name"] for model in models_data["models"] if model.get("available", True)]
            logging.info(f"Available models: {', '.join(available_models)}")
            return available_models
        else:
            logging.error(f"Failed to get models: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"Error getting available models: {str(e)}")
        return []

def query_model(model_name, prompt):
    """
    Send a query to the specified model via the PoeLocalServer API.

    Args:
        model_name (str): The name of the model to query
        prompt (str): The question or prompt to send

    Returns:
        tuple: (success (bool), response content or error message (str))
    """
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False  # Get the complete response at once
    }

    try:
        logging.info(f"Sending request to {model_name}...")
        response = requests.post(API_URL, json=payload, timeout=120)

        if response.status_code == 200:
            result = response.json()
            if "message" in result:
                return True, result["message"]["content"]
            else:
                return True, json.dumps(result, indent=2)
        else:
            error_msg = f"Error: Received status code {response.status_code}\n{response.text}"
            logging.error(error_msg)
            return False, error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        logging.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(error_msg)
        return False, error_msg

def save_response(response, model_name, filename=None):
    """
    Save the response to a file.

    Args:
        response (str): The text response to save
        model_name (str): The name of the model that generated the response
        filename (str, optional): Custom filename. If None, a timestamp-based name is used.

    Returns:
        str: Path to the saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lea_michele_tour_{model_name.lower().replace('-', '_').replace('.', '_')}_{timestamp}.md"

    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'w') as f:
        f.write(f"# Lea Michele Tour Plans\n\n")
        f.write(f"*Generated by {model_name} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(response)

    return filepath

def main():
    """
    Main function to query about Lea Michele's tour plans with fallback logic.
    """
    available_models = get_available_models()

    current_date = datetime.now().strftime("%B %d, %Y")
    prompt = f"""
    As of today, {current_date}, is Lea Michele planning to go on tour?

    Please provide:
    1. Information about any announced tour plans
    2. Her current projects and commitments
    3. Any recent statements she has made about touring
    4. Context about her career status and recent performances

    Format your response in Markdown with clear headings and bullet points.
    """

    if PRIMARY_MODEL in available_models:
        success, response = query_model(PRIMARY_MODEL, prompt)
        if success:
            logging.info(f"Successfully received response from {PRIMARY_MODEL}")
            filepath = save_response(response, PRIMARY_MODEL)
            print(f"\nResponse saved to: {filepath}")
            return
    else:
        logging.warning(f"{PRIMARY_MODEL} is not available")

    for model in FALLBACK_MODELS:
        if model in available_models:
            logging.info(f"Trying fallback model: {model}")
            success, response = query_model(model, prompt)
            if success:
                logging.info(f"Successfully received response from fallback model {model}")
                filepath = save_response(response, model)
                print(f"\nResponse saved to: {filepath}")
                print(f"\nNote: Used fallback model {model} instead of {PRIMARY_MODEL}")
                return

    error_message = "All models failed to provide a response. Please check the server status and try again."
    logging.error(error_message)
    print(error_message)

if __name__ == "__main__":
    main()
