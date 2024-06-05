import json
import time

import requests
import base64
from hashlib import blake2b


# Function to solve hash challenge
def solve_hash_challenge(challenge_id, message):
    # Decode base64
    message = base64.b64decode(message)

    attempt = 0  # Track number of attempts
    dots = ""  # String to hold dots

    # Find prefix to make blake2 hash with 2 leading bytes equal to 0
    prefix = b''

    print(f"\rSolving...")
    while True:
        test_message = prefix + message

        hash_bytes = blake2b(test_message, digest_size=32).digest()
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
    return response


# Main function
def main():
    # Hash challenge data
    input("Press any key to fetch new Hash challenge")
    print("\nFetch new challenge...")
    hash_challenge_response = requests.post('https://g5qrhxi4ni.execute-api.eu-west-1.amazonaws.com/Prod/hash').json()
    print(hash_challenge_response)
    input("\nPress any key to try to solve this challenge")

    # Solve hash challenge
    solve_response = solve_hash_challenge(hash_challenge_response['challengeId'], hash_challenge_response['message'])

    if solve_response.status_code == 200:
        print("\nSuccessfully solved challenge")
        print(f"message: {solve_response.json()['message']}")
    else:
        print("Something went wrong")


if __name__ == "__main__":
    main()
