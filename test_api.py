import requests
import json
from pprint import pprint

def test_openrouter_api():
    API_KEY = "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"
    BASE_URL = "https://openrouter.ai/api/v1"

    # First, let's get available models
    print("\n=== Available Models ===")
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "http://localhost:7860",
            "X-Title": "MY PRIDE Test"
        }
        
        models_response = requests.get(
            f"{BASE_URL}/models",
            headers=headers
        )
        models_response.raise_for_status()
        
        models_data = models_response.json()
        if isinstance(models_data, dict) and 'data' in models_data:
            for model in models_data['data']:
                print(f"- {model.get('id', 'Unknown')}: {model.get('name', 'No name')} ({model.get('pricing', {}).get('prompt', 'Unknown')} per prompt token)")
        else:
            print("Unexpected models response format:", json.dumps(models_data, indent=2))
            
    except requests.exceptions.RequestException as e:
        print(f"Network error getting models: {str(e)}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from models endpoint")
        print("Raw response:", models_response.text if 'models_response' in locals() else "No response")
    except Exception as e:
        print(f"Unexpected error getting models: {str(e)}")

    # Now test the chat completion
    print("\n=== Making Test API Call ===")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:7860",
        "X-Title": "MY PRIDE Test"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # Using a common model for testing
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'hello' if you can hear me."}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        print("Request Headers:", json.dumps(headers, indent=2))
        print("\nRequest Payload:", json.dumps(payload, indent=2))
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print("\nResponse Headers:", json.dumps(dict(response.headers), indent=2))
        
        try:
            response_data = response.json()
            if response.status_code == 200:
                print("\nSuccess! Response Body:", json.dumps(response_data, indent=2))
                if "choices" in response_data:
                    message = response_data["choices"][0]["message"]["content"]
                    print("\nBot Response:", message)
                else:
                    print("\nWarning: Successful response but no choices found in response")
            else:
                print("\nError! Response Body:", json.dumps(response_data, indent=2))
        except json.JSONDecodeError:
            print("\nError: Could not parse response as JSON")
            print("Raw response:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\nNetwork Error: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")

if __name__ == "__main__":
    print("Testing OpenRouter API connection...")
    test_openrouter_api()