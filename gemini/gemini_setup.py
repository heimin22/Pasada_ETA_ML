import requests
import os
from dotenv import load_dotenv

load_dotenv()

def geminiRequests(user_input):
    # this is the URL for the Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_ML"
    api_key = os.environ.get('GEMINI_API_ML')
        
    if not api_key:
        raise ValueError("wala akong nakitang API key rito gago")
    
    headers = { "Authorization": f"Bearer {api_key}" }
    data = {"query": user_input}
    response = requests.post(url, headers = headers, json = data)
    return response.json