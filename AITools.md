# AI Tools for Devin

This document provides information about AI extensions and tools available to Devin, including setup instructions, usage guidelines, and best practices.

## Poe Wrapper

The Poe Wrapper provides access to various AI models through Poe.com's API, enabling Devin to leverage different capabilities for a range of tasks.

### Available Models

The following models are currently prioritized for daily use:

| Model Name                | Description                                                    | Context Window | Tags   |
|---------------------------|----------------------------------------------------------------|----------------|--------|
| Web-Search               | Perplexity Sonar with web search capabilities                   | 8k             | latest |
| Claude-3.7-Sonnet        | Anthropic's Claude 3.7 Sonnet for everyday coding tasks         | 128k           | latest |
| Claude-3.7-Sonnet-Reasoning | Claude 3.7 Sonnet specialized for narrative writing and reasoning | 128k       | latest |
| o3-mini-high             | OpenAI's o3 model optimized for high-quality debugging          | 8k             | latest |
| GPT-4o-Mini              | GPT-4 Mini for quick tests and short responses                  | 8k             | latest |

### Setup and Launch

To use the Poe Wrapper:

1. **Start the Server**:
   ```bash
   cd ~/repos/PoeLocalServer
   source .venv/bin/activate
   ./run_server.sh
   ```
   Or:
   ```bash
   cd ~/repos/PoeLocalServer
   source .venv/bin/activate
   python -m poellama.main --verbose
   ```

2. **Verify Server Status**:
   The server will start on `http://0.0.0.0:8000`. Check for startup messages in the terminal to confirm it's running.

### Using the Poe Wrapper

#### File Organization

When creating scripts that use the Poe Wrapper:

- **Script Location**: Place Python scripts in the `PoeActions` directory at the project root. Use descriptive filenames indicating model and purpose (e.g., `claude_research_climate.py`).
- **Output Storage**:
  - General research: Save in `PoeActions` with a timestamp.
  - Project-specific content: Save in the relevant project directory.
  - Content for publishing: Save to the designated location in the project structure.

#### Making API Requests

Example template for making requests:

```python
import requests
import json

API_URL = "http://0.0.0.0:8000/api/chat"

payload = {
    "model": "MODEL_NAME",  # e.g., "Claude-3.5-Sonnet"
    "messages": [
        {"role": "user", "content": "Your prompt or question here"}
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

## Poe Query CLI Tool

This tool provides a command-line interface for querying various AI models through the PoeLocalServer API, with support for both streaming and non-streaming responses.

### Usage Instructions

1. Ensure the PoeLocalServer is running at `http://localhost:8000`.

2. Run the script with a prompt as a command-line argument:

```bash
python PoeActions/poe_query_cli.py "What is the current state of AI regulation in the US?"
```

3. Specify a model (default is Web-Search):

```bash
python PoeActions/poe_query_cli.py --model "GPT-4o-Mini" "What are the latest developments in AI image generation?"
```

4. Enable streaming mode for real-time responses:

```bash
python PoeActions/poe_query_cli.py --stream --model "Web-Search" "What are the latest developments in AI?"
```

### Features

- **Multiple Model Support**: Works with any model available in the PoeLocalServer
- **Response Format Handling**: Properly parses different response formats from various models
- **Streaming Mode**: Option to stream responses in real-time
- **Response Storage**: Saves responses to the `./perplexity_responses/` folder with model name and timestamp
- **Error Handling**: Robust error handling for various API response scenarios

### Notes

- The script uses `requests` for HTTP communication
- Special handling for Web-Search model responses to clean up incremental tokens
- Results are printed to the terminal and saved automatically

---

### Best Practices

1. **Choose the Right Model for the Task**:
   - **Web-Search (Perplexity)**: Best for timely, web-relevant queries and real-time summaries.
   - **Claude-3.7-Sonnet**: Ideal for everyday coding, refactoring, and walkthroughs.
   - **Claude-3.7-Sonnet-Reasoning**: Use for complex writing, outlining, and structured reasoning.
   - **o3-mini-high**: Reserved for challenging debugging and deep technical inspections.
   - **GPT-4o-Mini**: Great for unit tests, fast iterations, and short-form replies.

2. **Prompt Engineering**:
   - Be explicit about format expectations (e.g., Markdown, JSON, bullet points).
   - Include relevant context and constraints.
   - When in doubt, scaffold multi-step tasks with intermediate prompts.

3. **Code & Script Organization**:
   - Use consistent filenames with purpose and model (e.g., `sonnet_debug_parser.py`).
   - Save outputs with timestamps or versioned filenames for traceability.

4. **Error Handling & Robustness**:
   - Check response validity before processing.
   - Handle model downtimes gracefully.
   - Include retry logic where appropriate.

5. **Performance Considerations**:
   - Prefer lightweight models like GPT-4o-Mini for rapid prototyping.
   - Use streaming for longer queries to avoid timeouts and improve UX.
   - Minimize redundant prompts; reuse validated responses when possible.

6. **Output Hygiene**:
   - Sanitize and review model outputs before using in code or publication.
   - Implement parsers for structured formats.
   - Normalize responses for consistency across tools and models.



1. **Connection Issues**:
   - Check the server is running at `http://0.0.0.0:8000` or `http://localhost:8000`
   - Ensure the correct virtual environment is active.
   - Verify `.env` file contains valid API keys.

2. **Model Availability**:
   - Ensure the model is listed in `models.json`.
   - Look for rate limiting in server logs.
   - Switch to another model if needed.

3. **Response Quality**:
   - Refine prompts.
   - Choose a more capable model for complex tasks.
   - Simplify or segment complex queries.

---

_This document will be updated as new tools and extensions become available._
**Last updated:** April 5, 2025.
