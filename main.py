import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from browser_use import Agent

# Load environment variables from .env
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def main():
    # Define a simple wrapper LLM for Gemini
    class GeminiLLM:
        def __init__(self, model_name="gemini-2.0-flash"):
            self.provider = "google"   # required by browser-use
            self.model = model_name
            self.client = genai.GenerativeModel(model_name)

        async def ainvoke(self, prompt: str) -> str:
            response = self.client.generate_content(prompt)
            return response.text

    # Create LLM instance
    llm = GeminiLLM()

    # Task for the browser agent
    task = """
    Go to https://httpbin.org/forms/post and fill out the contact form with:
    - Customer name: John Doe
    - Telephone: 555-123-4567
    - Email: john.doe@example.com
    - Size: Medium
    - Topping: cheese
    - Delivery time: now
    - Comments: This is a test form submission

    Then submit the form and tell me what response you get.
    """

    # Create and run agent
    agent = Agent(task=task, llm=llm)
    history = await agent.run()

    # Print visited URLs
    print("\nVisited URLs:")
    for url in history.urls():
        print(url)


if __name__ == "__main__":
    asyncio.run(main())
