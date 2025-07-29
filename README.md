# Sample Project

This repository contains a small real estate prediction script and a simple web page. A new Python script `car_auction_agent.py` has been added that demonstrates how to create an OpenAI "assistant" (agent) that searches the web for car auctions and compares prices to the industry average.

The agent uses the OpenAI Python package (version 1.0+) and requires an `OPENAI_API_KEY` environment variable. When executed, it asks for the make and model of the car, creates an assistant with browser capability and retrieves auction information along with industry averages.

## Usage

```bash
pip install openai
export OPENAI_API_KEY=your-key
python car_auction_agent.py
```

Follow the on-screen prompts to get auction results.
