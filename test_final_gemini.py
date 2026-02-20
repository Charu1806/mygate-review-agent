from google import genai

client = genai.Client(
    api_key="AIzaSyDJLs6g6xkniOfKyoo8Q5GX4Rq7VkyLQnY",
    http_options={'api_version': 'v1beta'}
)

try:
    # Changed from 1.5-flash to 2.5-flash (which appeared in your list)
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents='Confirming connection to Gemini 2.5!'
    )
    print("Success! Gemini says:", response.text)
except Exception as e:
    print(f"Error: {e}")
