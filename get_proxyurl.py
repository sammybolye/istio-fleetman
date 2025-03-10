import requests


METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/proxy-url"
HEADERS = {"Metadata-Flavor": "Google"}

def get_url():
        response = requests.get(METADATA_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
        print(response.text)  

if __name__ == "__main__":
    get_url()
