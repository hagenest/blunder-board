import requests

# Replace YOUR_API_TOKEN with the API token you are using for authentication
API_TOKEN = "blunderboard-security-token"

# Set the API endpoint URL
url = "http://5.75.138.151:5000/api/get_evaluation"
wdl_api = "http://5.75.138.151:5000/api/get_wdl"

# Set the chess position and search depth
data = {
    "position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "depth": 20,
}

# Set the API token in the request header
headers = {"Authorization": API_TOKEN}

# Send a POST request to the API endpoint
response = requests.post(url, json=data, headers=headers)

# Print the response content from the server
if response.status_code == 200:
    print(response.json())

else:
    print("Error: " + response.json()["error"])

def api_wdl() -> str:
    """
    Returns the current wdl from the REST API
    :return: str
    """
    # Send a POST request to the API endpoint
    response2 = requests.post(wdl_api, json=data, headers=headers)
    if response2.status_code == 200:
        return response2.json()
    else:
        print("API Error: " + response2.json()["error"])
        return "API Error"


print(api_wdl())
