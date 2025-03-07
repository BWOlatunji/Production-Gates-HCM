import os
import requests


def download_files_from_text(text_file, folder_path):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Read the URLs from the text file
    with open(text_file, "r") as file:
        urls = file.readlines()

    # Iterate over each URL
    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace or newlines

        if url:
            try:
                # Parse the filename from the URL
                filename = os.path.basename(url)

                # Send HTTP request to download the file
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP errors

                # Check the Content-Type header to confirm it's a CSV
                content_type = response.headers.get("Content-Type")
                if "csv" in content_type:
                    # If filename doesn't have a CSV extension, add it
                    if not filename.endswith(".csv"):
                        filename += ".csv"

                    # Save the file to the specified folder
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "wb") as f:
                        f.write(response.content)

                    print(f"Downloaded and saved CSV: {filename}.")
                else:
                    print(
                        f"Warning: {filename} does not appear to be a CSV file. Content-Type: {content_type}"
                    )

            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")


# Execute
download_files_from_text("python_scripts/api_urls.txt", "data/downloads")
