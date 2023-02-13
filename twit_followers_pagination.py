import requests
import json,os


# Define the number of followers per page and the starting token
##############################################################################################################################################
##############           keep the count 1000 as to avoid the rate limit if keep 100 it would be each request for 100    ######################
##############################################################################################################################################
count = 1000
next_token = None
# parameters to be included
def get_params():
    return {"user.fields": "created_at","max_results":count,"pagination_token":next_token}

# authentication function using bearer token
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "DM Follower"
    return r

# Get followers Function
def get_followers(url,params):
    
    
    follows=[]
    while True:
        # Send the request to retrieve the followers
        response = requests.request("GET",url,auth=bearer_oauth ,params=params)
        print('response :',response)
        # Check the response status
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            # Get the list of followers
            followers = data["data"]
            follows.extend(followers)
            # Get the next token value
            next_token = data.get("meta", {}).get("next_token")
            if not next_token:
                break
        else:
            print(f"Error getting followers: {response.status_code}")
            break
    return follows

def main():
    

    # Define the user for whom you want to retrieve followers
    user_id='' 
    # Set up the API endpoint and authentication
    url= "https://api.twitter.com/2/users/{}/followers".format(user_id)

    # get parameters 
    params = get_params()
    # get followers
    json_response = get_followers(url,params)
    # number of followers
    print(f"Got Total {len(json_response)} Number of Followers")

    # save followers in json
    followers_json=json.dumps(json_response)
    with open("all_followers.json", "w") as outfile:
        outfile.write(followers_json)
    return json_response

if __name__ == "__main__":
    main()