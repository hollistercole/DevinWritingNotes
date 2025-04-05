# AI Tools for Devin

This document provides information about AI extensions and tools available to Devin, including setup instructions, usage guidelines, and best practices.

## Poe Wrapper

The Poe Wrapper provides access to various AI models through Poe.com's API, allowing Devin to leverage different AI capabilities for various tasks.

### Available Models

The following models are available through the Poe Wrapper:

| Model Name | Description | Token Cost | Context Window | Tags |
|------------|-------------|------------|----------------|------|
| Claude-3.5-Sonnet | Anthropic's Claude 3.5 Sonnet model | 326 | 200k | latest |
| Claude-3-Opus | Anthropic's most powerful Claude 3 model | 450 | 200k | powerful |
| GPT-4o | OpenAI's GPT-4o model | 400 | 128k | latest |
| Claude-3-Haiku | Anthropic's fastest Claude 3 model | 150 | 200k | fast |
| Llama-3-70b | Meta's Llama 3 70B parameter model | 200 | 8k | open-source |

### Setup and Launch

To use the Poe Wrapper:

1. **Start the Server**:
   ```bash
   cd ~/repos/PoeLocalServer
   source .venv/bin/activate
   ./run_server.sh
   ```
   
   Alternatively, you can run:
   ```bash
   cd ~/repos/PoeLocalServer
   source .venv/bin/activate
   python -m poellama.main --verbose
   ```

2. **Verify Server Status**:
   The server will start on `http://0.0.0.0:8000`. You can verify it's running by checking for the startup messages in the terminal.

### Using the Poe Wrapper

#### File Organization

When creating scripts that use the Poe Wrapper:

1. **Script Location**: 
   - Place Python scripts in the `PoeActions` directory at the root of your project
   - Use descriptive filenames that indicate the model and purpose (e.g., `claude_research_climate.py`)

2. **Output Storage**:
   - Save model outputs to appropriate locations based on the content type:
     - For general research: Save in the `PoeActions` directory with a timestamp
     - For project-specific content: Save in the relevant project directory
     - For content that will be published: Save directly to the appropriate location in the project structure

#### Making API Requests

Here's a template for making requests to the Poe Wrapper:

```python
import requests
import json

# Define the API endpoint
API_URL = "http://0.0.0.0:8000/api/chat"

# Define the request payload
payload = {
    "model": "MODEL_NAME",  # e.g., "Claude-3.5-Sonnet", "GPT-4o", etc.
    "messages": [
        {"role": "user", "content": "Your prompt or question here"}
    ],
    "stream": False  # Set to True for streaming responses
}

# Make the API request
response = requests.post(API_URL, json=payload)

# Process the response
if response.status_code == 200:
    result = response.json()
    if "message" in result:
        print(result["message"]["content"])
    else:
        print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

#### Example: Querying Claude-3.5-Sonnet

```python
import requests
import json

API_URL = "http://0.0.0.0:8000/api/chat"

payload = {
    "model": "Claude-3.5-Sonnet",
    "messages": [
        {"role": "user", "content": "What are the key considerations for sustainable urban planning?"}
    ],
    "stream": False
}

response = requests.post(API_URL, json=payload)

if response.status_code == 200:
    result = response.json()
    if "message" in result:
        print(result["message"]["content"])
    else:
        print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### Best Practices

1. **Model Selection**:
   - Use Claude models for nuanced reasoning, creative writing, and detailed analysis
   - Use GPT models for code generation, technical documentation, and general knowledge
   - Use Llama for tasks where an open-source model is preferred

2. **Prompt Engineering**:
   - Be specific about the format you want (Markdown, HTML, JSON, etc.)
   - Provide context and examples when needed
   - Break complex tasks into smaller, focused prompts

3. **Error Handling**:
   - Always implement proper error handling for API requests
   - Have fallback options if a specific model is unavailable
   - Consider implementing retries with exponential backoff for transient errors

4. **Resource Management**:
   - Be mindful of token usage, especially for larger models
   - Use streaming for long responses when appropriate
   - Consider batching multiple related queries into a single request when possible

5. **Output Processing**:
   - Validate and sanitize model outputs before using them in production
   - Implement parsing logic for structured outputs (JSON, tables, etc.)
   - Consider post-processing steps for formatting consistency

### Troubleshooting

If you encounter issues with the Poe Wrapper:

1. **Connection Issues**:
   - Verify the server is running at `http://0.0.0.0:8000`
   - Check that you're in the correct virtual environment
   - Ensure the `.env` file has valid API keys

2. **Model Availability**:
   - Confirm the model you're requesting is available in `models.json`
   - Check for any rate limiting messages in the server logs
   - Try a different model if one is consistently unavailable

3. **Response Quality**:
   - Refine your prompt for better results
   - Consider using a more capable model for complex tasks
   - Break down complex requests into simpler components

---

This document will be updated as new AI tools and extensions become available. Last updated: April 5, 2025.
