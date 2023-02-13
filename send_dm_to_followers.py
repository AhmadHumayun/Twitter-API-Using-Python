import os,json,requests
import sys
from time import sleep
# token regeneration function
from refresh_token import main as generate_token

##########################################################

##for testing the dm functionality
# participant_id is integer
participant_id=''

######################################################

def send_dm(text_message, participant_ids):
    request_body = {}

    # current directory
    _curr_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(_curr_dir)
    # load access token
    access = json.loads(open(f'{_curr_dir}/access_token.json', 'r').read())

    headers = {
        "Authorization": "Bearer {}".format(access['access_token']),
        "Content-Type": "application/json",
        "User-Agent": "DM Follower",
        "X-TFE-Experiment-environment": "staging1",
        "Dtab-Local": "/s/gizmoduck/test-users-temporary => /s/gizmoduck/gizmoduck"
    }
    #   endpoint for sending dm
    POST_DM_URL = "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
    
    # replace participant id string with actual id
    request_url = POST_DM_URL.replace(':participant_id', str(participant_ids))
    request_body['text'] = text_message
    json_body = json.dumps(request_body)
    #Send DM
    response = requests.request("POST", request_url, headers=headers, json=json.loads(json_body))
    # if token expired generate the token and send the request again
    if response.status_code==401:
        generate_token()
        access = json.loads(open(f'{_curr_dir}/access_token.json', 'r').read())
        headers = {
        "Authorization": "Bearer {}".format(access['access_token']),
        "Content-Type": "application/json",
        "User-Agent": "DM Follower",
        "X-TFE-Experiment-environment": "staging1",
        "Dtab-Local": "/s/gizmoduck/test-users-temporary => /s/gizmoduck/gizmoduck"
        }
        response = requests.request("POST", request_url, headers=headers, json=json.loads(json_body))
        print("Credentials Refreshed")
    

    return response

def main():

    # current directory
    _curr_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(_curr_dir)

    # get followers from followers json file
    followers = json.loads(open(f'{_curr_dir}/all_followers.json', 'r').read())

    # get followers to whom dm had already been sent from sent_dm json file
    sent_dm = json.loads(open(f'{_curr_dir}/sent_dm.json', 'r').read())

    # get ids for all sent dm followers
    sent_dm_ids = [i['id'] for i in sent_dm]
    count=0
    for i in followers:
    # check followers to whom dm is not sent yet
        if i['id'] not in sent_dm_ids:
            # DM Text
            text_message="Thanks, for follow"
            # send DM
            response = send_dm(text_message, i['id'])
            count+=1
            # sleep for 15 mins if rate limit is about to reach
            if count==400:
                sys.exit(1)
            if int(response.headers['x-rate-limit-remaining'])==1:
                sleep(60*15)
            # check if DM not sent successfully
            if response.status_code != 201:
                print("Request returned an error: {} {}".format(response.status_code, response.text))
                print('SOMETHING HAPPENED KINDLY CHECK THE CODE')
                exit(1)
            else:
                # print(f"Response code: {response.status_code}")
                sent_dm.append(i)
                sent_dm_json=json.dumps(sent_dm)
                # if DM sent successfully add it to the sent_dm json file
                with open("sent_dm.json", "w") as outfile:
                    outfile.write(sent_dm_json)
                outfile.close()
                print(f'DM Sent To {i["username"]}')
    
if __name__ == "__main__":
    main()