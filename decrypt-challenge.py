import base64
import json

import nacl
import requests
from nacl.secret import SecretBox

BASE_URL = 'https://g5qrhxi4ni.execute-api.eu-west-1.amazonaws.com/Prod/decrypt'


def decrypt_challenge(challenge_data):
    try:
        # Validate required keys
        required_keys = {"challengeId", "ciphertext", "key", "nonce"}
        if not all(key in challenge_data for key in required_keys):
            raise ValueError("Invalid challenge data: missing required keys")

        # Decode base64-encoded data
        ciphertext = base64.b64decode(challenge_data["ciphertext"])
        key = base64.b64decode(challenge_data["key"])
        nonce = base64.b64decode(challenge_data["nonce"])

        # Use SecretBox from pynacl (libsodium binding)
        box = SecretBox(key)
        decrypted_message = box.decrypt(ciphertext, nonce)

        return {
            "plaintext": base64.b64encode(decrypted_message).decode('utf-8')
        }


    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid challenge data: {e}")


if __name__ == '__main__':
    try:
        input("Press any key to fetch new Decrypt challenge")
        print("\nFetching challenge...")

        decrypt_challenge_response = requests.post(BASE_URL).json()
        print(decrypt_challenge_response)

        input("\nPress any key to try to solve this challenge")
        challenge_payload = decrypt_challenge(decrypt_challenge_response)
        headers = {"Content-Type": "application/json"}
        json_payload = json.dumps(challenge_payload)
        response = requests.delete(f"{BASE_URL}/{decrypt_challenge_response['challengeId']}", data=json_payload, headers=headers)

        # Validate if challenge was success
        if response.status_code == 204:
            print("Successful solved decrypt challenge")
        else:
            print("Something went wrong")
    except ValueError as e:
        print(f"Error: {e}")
