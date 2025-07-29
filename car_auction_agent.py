import os
import time
import openai

"""A simple command-line tool that uses OpenAI's assistant (agent) API
   to search for car auctions and check industry averages.

   You must provide an OPENAI_API_KEY environment variable for this to work.
"""

# Ensure API key
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable")

openai.api_key = os.environ["OPENAI_API_KEY"]

# Prompt user for car details
car = input("Enter the make and model of the car you're looking for: ")

# Create an assistant with browser/search capability
assistant = openai.beta.assistants.create(
    name="Car Auction Assistant",
    instructions=(
        "You are an assistant that searches for auction listings for cars and "
        "compares them to the industry average price using online sources."
    ),
    tools=[{"type": "browser"}]
)

# Create a thread and post the initial question
thread = openai.beta.threads.create()
openai.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"I am looking for auctions for a {car}. Please find current auctions "
            "and tell me the industry average price."
)

# Run the assistant and wait for completion
run = openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
while run.status not in ("completed", "failed", "cancelled"):
    time.sleep(1)
    run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

# Print out all assistant messages
messages = openai.beta.threads.messages.list(thread_id=thread.id)
for msg in messages:
    if msg.role == "assistant":
        print(msg.content[0].text.value)
