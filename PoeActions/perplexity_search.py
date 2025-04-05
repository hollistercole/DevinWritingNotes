import os
import json
import asyncio
import logging
import sys  # Import the sys module
from pathlib import Path
import httpx
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create responses directory if it doesn't exist
responses_dir = Path("./perplexity_responses")  # Current directory
responses_dir.mkdir(exist_ok=True)
logging.info(f"Responses will be saved to: {responses_dir.absolute()}")


class PerplexityTester:
    def __init__(self, prompt: str):
        # Get current date in the desired format
        current_date = datetime.now().strftime("%B %d, %Y")  # Format: April 5, 2025

        # Append "as of [today's date]" to the prompt
        self.prompt = f"{prompt} as of [{current_date}]"

        # Test messages with dynamic date
        self.test_messages = [
            {
                "role": "user",
                "content": self.prompt
            }
        ]

        # Initialize HTTP client
        self.client = httpx.AsyncClient()

    def save_response(self, response_text: str):
        """Save response to a file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = responses_dir / f"perplexity_streaming_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Prompt: {self.prompt}\n")  # Save the prompt
            f.write("\nResponse:\n")
            f.write(response_text)

        logging.info(f"Response saved to: {filename.absolute()}")
        return filename

    async def streaming_response(self, model: str = "Web-Search"):
        """Get a streaming response from the specified model."""
        try:
            # Prepare the request
            url = "http://localhost:8000/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
            }
            data = {
                "model": model,
                "messages": self.test_messages,
                "temperature": 0.7,
                "stream": True
            }

            # Make the request
            logging.info(f"Getting streaming response with model: {model}")
            try:
                async with self.client.stream("POST", url, json=data, headers=headers, timeout=30.0) as response:
                    if response.status_code == 200:
                        final_response = ""
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                data = line[6:]  # Remove "data: " prefix
                                if data == "[DONE]":
                                    break

                                try:
                                    chunk = json.loads(data)
                                    if "choices" in chunk and chunk["choices"]:
                                        choice = chunk["choices"][0]

                                        # Extract content from delta if present
                                        if "delta" in choice and "content" in choice["delta"]:
                                            content = choice["delta"]["content"]
                                            final_response += content  # Accumulate content

                                        # Check if this is the final message
                                        finish_reason = choice.get("finish_reason")
                                        if finish_reason == "stop":
                                            logging.info("End of stream detected.")
                                            break  # Exit loop when the last message is received
                                except json.JSONDecodeError as e:
                                    logging.warning(f"Failed to parse chunk: {data}\nError: {str(e)}")
                                    continue

                        # Output the final response
                        if final_response:
                            logging.info(f"Received final response: {final_response[:100]}...")
                            self.save_response(final_response)
                            print(final_response)  # Print the response
                            return True
                        else:
                            logging.error("No response content received")
                            return False
            except httpx.ConnectError:
                logging.error(f"Failed to connect to server at {url}. Is the server running?")
                return False
            except Exception as e:
                logging.error(f"Request failed: {str(e)}", exc_info=True)
                return False

        except Exception as e:
            logging.error(f"Error during streaming test: {str(e)}", exc_info=True)
            return False

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


async def main():
    """Run the streaming response."""
    if len(sys.argv) < 2:
        print("Usage: python your_script.py \"Your prompt here\"")
        sys.exit(1)

    prompt = sys.argv[1]

    tester = PerplexityTester(prompt)
    try:
        # Get streaming response
        logging.info("Getting streaming response...")
        streaming_success = await tester.streaming_response()

        # Report results
        if not streaming_success:
            logging.error("Streaming failed. Check the logs for details.")

    finally:
        await tester.close()


if __name__ == "__main__":
    asyncio.run(main())
