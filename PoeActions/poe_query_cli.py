"""
Poe Query CLI - A command-line tool for querying models via the PoeLocalServer API.

This script allows users to send queries to various models through the PoeLocalServer API.
It supports both streaming and non-streaming responses.

Usage:
    python poe_query_cli.py "Your query here"
    python poe_query_cli.py --model "Web-Search" "Your query here"
    python poe_query_cli.py --stream --model "Web-Search" "Your query here"

Author: Devin AI
Date: April 5, 2025
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime

RESPONSES_DIR = Path("./perplexity_responses")
RESPONSES_DIR.mkdir(exist_ok=True)

API_URL = "http://localhost:8000/api/chat"

def save_response(prompt, response_text, model):
    """
    Save response to a file with timestamp.
    
    Args:
        prompt (str): The original query
        response_text (str): The response text to save
        model (str): The model used for the query
        
    Returns:
        Path: The path to the saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = RESPONSES_DIR / f"{model.lower().replace('-', '_')}_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Query: {prompt}\n\n")
        f.write(f"*Generated by {model} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(response_text)
    
    print(f"Response saved to: {filename}")
    return filename

def query_model(prompt, model="Web-Search", stream=False):
    """
    Send a query to the specified model and return the response.
    
    Args:
        prompt (str): The query to send
        model (str): The model to use
        stream (bool): Whether to use streaming mode
        
    Returns:
        str: The model's response
    """
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": stream
    }
    
    print(f"Sending query to {model}: {prompt[:50]}...")
    
    if stream:
        return stream_response(payload)
    else:
        return get_response(payload)

def get_response(payload):
    """
    Get a complete response from the model.
    
    Args:
        payload (dict): The request payload
        
    Returns:
        str: The complete response
    """
    try:
        response = requests.post(API_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            if "choices" in result and result["choices"]:
                content = result["choices"][0]["message"]["content"]
                return content
                
            elif "message" in result and "content" in result["message"]:
                content = result["message"]["content"]
                
                if payload["model"] == "Web-Search" and "Searching..." in content:
                    return clean_websearch_response(content)
                
                return content
            else:
                return f"Error: Unexpected response format: {json.dumps(result)}"
        else:
            return f"Error: Received status code {response.status_code}\n{response.text}"
            
    except Exception as e:
        return f"Request error: {str(e)}"

def clean_websearch_response(content):
    """
    Clean up Web-Search response by removing incremental tokens and searching messages.
    
    Args:
        content (str): The raw Web-Search response
        
    Returns:
        str: The cleaned response
    """
    lines = content.split('\n')
    clean_lines = []
    
    seen_content = set()
    for line in reversed(lines):
        if not line or line.startswith("Searching"):
            continue
            
        stripped = line.strip()
        is_duplicate = False
        for existing in seen_content:
            if stripped in existing or existing in stripped:
                is_duplicate = True
                break
                
        if not is_duplicate:
            clean_lines.append(line)
            seen_content.add(stripped)
    
    clean_lines.reverse()
    
    return '\n'.join(clean_lines)

def stream_response(payload):
    """
    Stream a response from the model.
    
    Args:
        payload (dict): The request payload
        
    Returns:
        str: The complete streamed response
    """
    try:
        final_response = ""
        model = payload["model"]
        
        with requests.post(API_URL, json=payload, stream=True, timeout=120) as response:
            if response.status_code != 200:
                return f"Error: Received status code {response.status_code}\n{response.text}"
            
            for line in response.iter_lines():
                if not line:
                    continue
                    
                line = line.decode('utf-8')
                if not line.startswith("data: "):
                    continue
                    
                data = line[6:]  # Remove "data: " prefix
                
                if data == "[DONE]":
                    break
                
                try:
                    chunk = json.loads(data)
                    
                    if "choices" in chunk and chunk["choices"]:
                        choice = chunk["choices"][0]
                        
                        if "delta" in choice and "content" in choice["delta"]:
                            content = choice["delta"]["content"]
                            final_response += content
                            print(content, end="", flush=True)
                        
                        if choice.get("finish_reason") == "stop":
                            break
                    
                    elif "message" in chunk and "content" in chunk["message"]:
                        content = chunk["message"]["content"]
                        
                        if model == "Web-Search" and "Searching..." in content:
                            content = clean_websearch_response(content)
                        
                        final_response = content  # Replace with full content
                        print(content, flush=True)
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        print()  # Add a newline after streaming completes
        
        if model == "Web-Search" and "Searching..." in final_response:
            final_response = clean_websearch_response(final_response)
            
        return final_response
        
    except Exception as e:
        print(f"\nStreaming error: {str(e)}")
        return f"Streaming error: {str(e)}"

def main():
    """Parse arguments and run the query."""
    parser = argparse.ArgumentParser(description="Query models via the PoeLocalServer API")
    parser.add_argument("prompt", help="The query to send to the model")
    parser.add_argument("--model", "-m", default="Web-Search", 
                        help="Model to use (default: Web-Search)")
    parser.add_argument("--stream", "-s", action="store_true", 
                        help="Use streaming mode")
    
    args = parser.parse_args()
    
    response = query_model(args.prompt, args.model, args.stream)
    
    if response:
        saved_file = save_response(args.prompt, response, args.model)
        print(f"Query complete. Response saved to {saved_file}")
    else:
        print("No response received")

if __name__ == "__main__":
    main()
