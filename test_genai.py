from google import genai

client = genai.Client(api_key="AIzaSyCSElHmYeDKEh0EF-msGmwsIN5eW35UISE")
system_prompt = "You are an astrologer.\n\nUser: hi\nAstrologer: hello\nUser: what is my sign?\nAstrologer: "

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=system_prompt
    )
    print("Success:", response.text)
except Exception as e:
    print("Error:", type(e), e)
