from google import genai

client = genai.Client(
    api_key="AIzaSyDJLs6g6xkniOfKyoo8Q5GX4Rq7VkyLQnY",
    http_options={'api_version': 'v1beta'}
)

try:
    # Let's first print what models you actually have access to
    print("Checking available models...")
    for m in client.models.list():
        print(f"Found: {m.name}")
    
    print("-" * 30)

    # Use the most explicit name possible
    response = client.models.generate_content(
        model='models/gemini-1.5-flash',
        contents='Tell me one short fact about space.'
    )
    print("Success! Gemini says:", response.text)

except Exception as e:
    print(f"Caught an error: {e}")
