import requests
import os
from dotenv import load_dotenv

def gemini_test(user_input, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "HAHAHAHAHA bobo ka raw"
        
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_ML")
    if not api_key:
        raise ValueError("wala akong nakitang API key rito gago")
        exit(1)
        
    print("Welcome kupal")
    print("Type mo yung prompt mo, tapos pindutin mo yung Enter para sa response")
    print("Kapag ayaw mo na my nigga, type mo 'exit'")
    
    while True:
        user_input = input("\nMe: ").strip()
        if user_input.lower() == "exit":
            print("Bye kupal!")
            break
        if not user_input:
            print("Bawal blangko tarantado, type mo yung prompt mo.")
            continue

        response = gemini_test(user_input, api_key)
        print(f"Gemini: {response}")