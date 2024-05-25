import json

import requests
import base64
from hashlib import blake2b
# Function to solve hash challenge
def solve_hash_challenge(challenge_id, message):
    # Decode base64
    message = base64.b64decode(message)

    # Find prefix to make blake2 hash with 2 leading bytes equal to 0
    prefix = b''

    while True:
        test_message = prefix + message

        hash_bytes = blake2b(test_message, digest_size=32).digest()
        print(f"Hash: {hash_bytes[:4]}")  # Print first 4 bytes of hash
        if hash_bytes[0] == 0 and hash_bytes[1] == 0:
            break  # Found a prefix!
        prefix += b'\x00'  # Increment prefix when no prefix found to start hash with 2 leading bytes as 0

    # Prepare solution payload decoding
    solution = {'prefix': base64.b64encode(prefix).decode("utf-8")}

    # Put solution in json format
    json_string = json.dumps(solution)

    # Send DELETE request with solution payload
    url = f"https://g5qrhxi4ni.execute-api.eu-west-1.amazonaws.com/Prod/hash/{challenge_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, data=json_string, headers=headers)

    # Print response to see if delete was a success
    print(response.json())
    print(response.status_code)


# Main function
def main():
    # TODO: Do a request to get the data and solve in one flow?
    # Hash challenge data
    hash_challenge = {
        "challengeId": "4124509614",
        "message": "OMCGutwRy4Pd56RDDI7VuaaqeUjF0I9zxu2qVVUb4dSqzxreQeH2I4OXrQAM3nnP+0xkXRwkEMd62ffBVVn+lg==",
        "attemptsRemaining": "3"
    }

    # Solve hash challenge
    solve_hash_challenge(hash_challenge['challengeId'], hash_challenge['message'], hash_challenge['attemptsRemaining'])


if __name__ == "__main__":
    main()
