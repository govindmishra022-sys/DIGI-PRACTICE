from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyCSElHmYeDKEh0EF-msGmwsIN5eW35UISE")

contents = [
    types.Content(role="user", parts=[types.Part.from_text(text="Hi, I am an Aries. What's my lucky number?")])
]

config = types.GenerateContentConfig(
    system_instruction="You are a mystical astrologer."
)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=contents,
        config=config
    )
    print("Success 2.0:", response.text)
except Exception as e:
    print("Error 2.0:", type(e), e)

try:
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=contents,
        config=config
    )
    print("Success 1.5:", response.text)
except Exception as e:
    print("Error 1.5:", type(e), e)
