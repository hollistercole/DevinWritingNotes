"""
Script to query Claude-3.7-Sonnet about the top 5 things to do in Zermatt, Switzerland
using the PoeLocalServer.
"""

import requests
import json
import sys
import os
from datetime import datetime

API_URL = "http://0.0.0.0:8000/api/chat"

def query_claude(prompt):
    """
    Send a query to Claude-3.7-Sonnet via the PoeLocalServer API.
    
    Args:
        prompt (str): The question or prompt to send to Claude
        
    Returns:
        str: Claude's response or error message
    """
    payload = {
        "model": "Claude-3.7-Sonnet",  # Specify the model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False  # Set to False to get the complete response at once
    }
    
    try:
        print(f"Sending request to Claude-3.7-Sonnet...")
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "message" in result:
                return result["message"]["content"]
            else:
                return json.dumps(result, indent=2)
        else:
            return f"Error: Received status code {response.status_code}\n{response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def save_response(response, filename=None):
    """
    Save the response to a file.
    
    Args:
        response (str): The text response to save
        filename (str, optional): Custom filename. If None, a timestamp-based name is used.
    
    Returns:
        str: Path to the saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"claude_zermatt_{timestamp}.md"
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w') as f:
        f.write("# Top 5 Things to Do in Zermatt, Switzerland\n\n")
        f.write(f"*Generated by Claude-3.7-Sonnet on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(response)
    
    return filepath

def main():
    prompt = """
    What are the top 5 things to do in Zermatt, Switzerland? 
    
    For each attraction, please provide:
    1. A brief description
    2. Why it's worth visiting
    3. Practical tips for visitors
    
    Format your response in Markdown with clear headings and bullet points.
    """
    
    response = query_claude(prompt)
    
    print("\nResponse from Claude-3.7-Sonnet:")
    print("-" * 50)
    print(response)
    print("-" * 50)
    
    filepath = save_response(response)
    print(f"\nResponse saved to: {filepath}")

if __name__ == "__main__":
    main()
