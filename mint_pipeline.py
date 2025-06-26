import os
import json
import requests

NFT_STORAGE_API_KEY = os.getenv("NFT_STORAGE_API_KEY")

def upload_file_to_nft_storage(filepath):
    url = "https://api.nft.storage/upload"
    headers = {
        "Authorization": f"Bearer {NFT_STORAGE_API_KEY}",
    }
    with open(filepath, "rb") as f:
        files = {"file": f}
        response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        res_json = response.json()
        return "https://ipfs.io/ipfs/" + res_json["value"]["cid"]
    else:
        raise Exception(f"Upload failed: {response.status_code} {response.text}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mint pipeline for Toro Deck NFTs")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--metadata", required=True, help="Path to metadata JSON file")
    args = parser.parse_args()

    print("Uploading image...")
    image_url = upload_file_to_nft_storage(args.image)
    print(f"Image uploaded: {image_url}")

    print("Loading metadata...")
    with open(args.metadata, "r") as f:
        metadata = json.load(f)

    metadata["image"] = image_url

    print("Uploading metadata...")
    temp_metadata_path = "temp_metadata.json"
    with open(temp_metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    metadata_url = upload_file_to_nft_storage(temp_metadata_path)
    os.remove(temp_metadata_path)

    print(f"Metadata uploaded: {metadata_url}")
    print("Mint URI ready:", metadata_url)
    print("Use this URI with your minting tool or platform.")

if __name__ == "__main__":
    if not NFT_STORAGE_API_KEY:
        print("Error: Set NFT_STORAGE_API_KEY environment variable before running.")
    else:
        main()