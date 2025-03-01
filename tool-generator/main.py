import requests
import os
from urllib.parse import urlparse

def download_from_url(url, output_path=None):
    try:
        # Send GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # If no output path is specified, use the filename from URL
        if not output_path:
            output_path = os.path.basename(urlparse(url).path)
            if not output_path:
                output_path = 'downloaded_file'
        
        # Write the content to a file
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        
        print(f"Successfully downloaded to: {output_path}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    url = "https://polygon.io/docs/stocks/get_vx_reference_tickers__id__events"
    output_path = "./tool-generator/get_vx_reference_tickers__id__events.html"
    
    if not output_path:
        output_path = None
    
    download_from_url(url, output_path)
