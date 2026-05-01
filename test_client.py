import requests
import io
from PIL import Image

def create_test_image(filename="test_clean.jpg"):
    img = Image.new('RGB', (400, 300), color = 'red')
    img.save(filename, format='JPEG', quality=95)
    return filename

def test_api():
    url = "http://localhost:8000/v1/analyze"
    filename = create_test_image()
    
    with open(filename, "rb") as f:
        # Note we are simulating a local call, so API key is optional, but we can pass it
        headers = {"X-API-Key": "sandbox_sk_12345"}
        files = {"file": ("test_clean.jpg", f, "image/jpeg")}
        response = requests.post(url, files=files, headers=headers)
        
    print("Status Code:", response.status_code)
    print("Response JSON Keys:", response.json().keys() if response.status_code == 200 else response.text)
    if response.status_code == 200:
        data = response.json()
        print("Risk Level:", data.get("risk_level"))
        print("Risk Score:", data.get("risk_score"))

if __name__ == "__main__":
    test_api()
