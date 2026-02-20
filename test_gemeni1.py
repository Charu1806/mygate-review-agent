from google import genai
from google.genai import types

# We explicitly set the version to 'v1' to avoid the 404 on 'v1beta'
client = genai.Client(
    api_key="AIzaSyAPXodhg-dkoJAxFw-HefGQanO3rxdMuZk",
    http_options={'api_version': 'v1'}
)

try:
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Confirm if you can hear me!'
    )
    if response.text:
        print("Success! Gemini says:", response.text)
    else:
        print("Received an empty response.")
except Exception as e:
    print(f"Caught an error: {e}")
