import requests,json,os,sys





def main():
    client_id = ""
    client_secret = ""
    # current directory
    _curr_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(_curr_dir)
    # load access token
    access = json.loads(open(f'{_curr_dir}/access_token.json', 'r').read())
    # # # create the payload
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": access["refresh_token"],
        "client_id": client_id,
        # "client_secret": client_secret
    }
    headers={
    "Content-Type": "application/x-www-form-urlencoded"
    }
    # # send the request to obtain new access token and secret
    url = "https://api.twitter.com/2/oauth2/token"
    response = requests.post(url, data=payload,headers=headers)
    # response = requests.post(url, data=payload)

    # parse the response
    response_data = json.loads(response.text)
    token_dict=json.dumps(response_data)
    # Writing to sample.json
    with open("access_token.json", "w") as outfile:
        outfile.write(token_dict)
    # print(response_data)
    # print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))

if __name__ == "__main__":
    main()