print("Hello World")
import openai

# Set your API key
api_key = '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'
openai.api_key = api_key

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Use the ChatGPT model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": "Why did the chicken cross the road?"},
        {"role": "user", "content": "I don't know, why did the chicken cross the road?"}
    ]
)

# Extract the assistant's reply
assistant_reply = response['choices'][0]['message']['content']
print(assistant_reply)
