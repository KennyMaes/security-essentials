import base64
import json

import nacl
import requests
from nacl.secret import SecretBox


def decrypt_challenge(challenge_data):
    try:
        # Validate required keys
        required_keys = {"challengeId", "ciphertext", "key", "nonce"}
        if not all(key in challenge_data for key in required_keys):
            raise ValueError("Invalid challenge data: missing required keys")

        # Decode base64-encoded data
        ciphertext = base64.b64decode(challenge_data["ciphertext"])
        print(ciphertext)
        key = base64.b64decode(challenge_data["key"])
        print(key)
        nonce = base64.b64decode(challenge_data["nonce"])
        print(nonce)

        # Use SecretBox from pynacl (libsodium binding)
        box = SecretBox(key)
        decrypted_message = box.decrypt(ciphertext, nonce)

        print('create payload')

        return {
            "plaintext": base64.b64encode(decrypted_message).decode('utf-8')
        }


    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid challenge data: {e}")


if __name__ == '__main__':
    try:
        challenge_data = {
            "challengeId": "821789417",
            "key": "BbpdPT7UJDvnfV1ms5CYqx7abFBZ6wknZfgs3hWA/J4=",
            "ciphertext": "02X89onti6ew1robvXXEYg854+45DoIqvI2R94mjxu5IBhKPfNJ2J8gxVPPHjybmMfyP/iyeqyfOqzLbo0c9+br7QQ0p6JGtDPZgIiDfHJzW2dbyqS1BMtU2h1044CEonT0F7DvZnLhb+5Zi2wwiso46u4TT9atXQlAlHD+3vXXBdNlHDSRGzMhoDh+wuGSo",
            "nonce": "U4d9U/oVRYidcPZPS5QcMv9eKZ+8R037"
        }
        payload = decrypt_challenge(challenge_data)
        print(payload)
        url = f"https://g5qrhxi4ni.execute-api.eu-west-1.amazonaws.com/Prod/decrypt/{challenge_data['challengeId']}"
        headers = {"Content-Type": "application/json"}
        json_payload = json.dumps(payload)
        response = requests.delete(url, data=json_payload, headers=headers)

        # Print response to see if delete was a success
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
