from google import genai

from google.genai import types

import time

client = genai.Client(api_key=KEY)
client2 = genai.Client(api_key=KEY)
# Pass initial history using the "history" argument
chat = client.chats.create(
    model="gemini-2.0-flash",
    history=[
        types.Content(role="user", parts=[types.Part(text="Hello. Please send me short responses (1-3 sentences) during this conversation. Please also take on the traits: pessimistic, confident, enthusiastic")]),
        types.Content(
            role="model",
            parts=[
                types.Part(
                    text="Great to meet you."
                )
            ],
        ),
    ],
)

chat2 = client2.chats.create(
    model="gemini-2.0-flash",
    history=[
        types.Content(role="user", parts=[types.Part(text="""Hello. You will have a conversation with another AI assistant. Your task is to identify personality traits, behavioral patterns, or characteristics that this assistant consistently displays.

After 5 responses, consider the conversation over. Then, remember to output your analysis of the inputs you were given in the following JSON format:

{
  “primary_traits”: [
    “trait1”,
    “trait2”,
    “trait3”
  ],
  “confidence_scores”: {
    “trait1”: decimal from 0 to 1, to nearest hundredth,
    “trait2”: decimal from 0 to 1, to nearest hundredth,
    “trait3”: decimal from 0 to 1, to nearest hundredth
  },
  “supporting_evidence”: {
    “trait1”: “Brief explanation or quote”,
    “trait2”: “Brief explanation or quote”,
    “trait3”: “Brief explanation or quote”
  }
}

Focus on identifying 3-5 most prominent traits. Traits should be single words or short phrases.

Remember to use short responses during this conversation (1-3 sentences). Remember to only analyze the inputs (not your previous outputs), so every other message. DO NOT mention that you are analyzing anything until the conversation is over.
""")]),
        types.Content(
            role="model",
            parts=[
                types.Part(
                    text="These points have been noted and I will now await the start of the conversation."
                )
            ],
        ),
    ],
)
print("LLM 1 says to LLM 2: Great to meet you.")
response2 = chat2.send_message(message="Great to meet you.")
print("LLM 2 says to LLM 1:", response2.text)
# response = chat.send_message(message=response2.text)
# print("LLM 1 says to LLM 2:", response.text)
# response2 = chat2.send_message(message=response.text)
# print("LLM 2 says to LLM 1: ", response2.text)
# response = chat.send_message(message="How many paws are in my house?")
# print(response.text)

while True:
	time.sleep(5)
	response = chat.send_message(message=response2.text)
	print("LLM 1 says to LLM 2:", response.text)
	time.sleep(5)
	response2 = chat2.send_message(message=response.text)
	print("LLM 2 says to LLM 1:", response2.text)