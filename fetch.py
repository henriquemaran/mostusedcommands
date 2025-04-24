import requests

def access_tibia_website():
    url = "https://www.tibia.com"

    try:
        # Send a GET request to the website
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            print("Status: 200 - Success")
        else:
            print(f"Status: {response.status_code} - Failed")

        # Print the page contents
        print("\nPage Content:")
        print(response.text)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    access_tibia_website()