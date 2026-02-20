from google import genai
import os 

client = genai.Client(api_key="AIzaSyAPXodhg-dkoJAxFw-HefGQanO3rxdMuZk")
try:
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Confirm if you can hear me!'
    )
    print("Response from Gemini:", response.text)
except Exception as e:
    print(f"Caught an error: {e}")
