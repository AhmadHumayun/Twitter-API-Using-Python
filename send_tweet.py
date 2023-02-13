import requests
import json,os,sys

def send_tweet(text_message):
    # Set up the API endpoint and authentication
    _curr_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(_curr_dir)
    access = json.loads(open(f'{_curr_dir}/access_token.json', 'r').read())
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": "Bearer {}".format(access['access_token']),
        "Content-Type": "application/json",
    }

    # Define the tweet text
    data = {
        "text": text_message
        # "visibility": "public",
    }
    
    # Send the request to post the tweet
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print('response : ',response)
    # Check the response status
    if response.status_code == 201:
        print("Tweet sent successfully!")
    else:
        print(f"Error sending tweet: {response.status_code}")


def main():
    # username
    participant_names = 'unknown'
    print(participant_names)

    text_message=f"Thanks @{participant_names[0]}, for follow"
    print(text_message)
    response = send_tweet(text_message )
    print(response)
    # print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
