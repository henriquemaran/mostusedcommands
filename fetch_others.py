import requests
import json

def access_tibia_data_api():
    url = "https://api.tibiadata.com/v4/character/Yakuti%20do%20juninho"
    headers = {'accept': 'application/json'}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Status: 200 - Success")
            data = response.json()

            # Extract "other_characters"
            other_characters = data.get("character", {}).get("other_characters", [])
            print("Other Characters:")

            # Print "name" and "status" of each character
            for character in other_characters:
                name = character.get("name", "Unknown")
                status = character.get("status", "Unknown")
                print(f"- Name: {name}, Status: {status}")
        else:
            print(f"Status: {response.status_code} - Failed")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    access_tibia_data_api()
