# run an API call
from openai import OpenAI
client0 = OpenAI()

response0 = client0.responses.create(
    model="gpt-5-nano",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response0.output_text)

# analyze image (other possibilities: file link, or upload from local)
client1 = OpenAI()

response1 = client1.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "What teams are playing in this image?",
                },
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
                }
            ]
        }
    ]
)

print(response1.output_text)

# extend model with tools (i.e. WebSearch)
client2 = OpenAI()

response2 = client2.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input="What was a positive news story from today?"
)

print(response2.output_text)
