# Twitter-API-Using-Python
Testing Different Endpoints of Twitter API using Python
## Authentication:
  1. First Create App in Developer Console.
  2. Allow Oauht2.0 native in settings.
  3. get client id from keys tab
  4. Use client_id in **generate_access_token.py** Script and generate access token
  5. access token gets expired after 2 hours so will have to use refresh token to regenerate access token.
  6. for using refresh_token to generate access_token use **refresh_token.py** script.
## Get Followers:
  1. To get followers first you need to get user id.
  2. You can get User id from **https://tweeterid.com/** .
  3. add the user id in get_followers.py script and run it.
  4. all_followers.json file will be created which will have all the followers data.
  5. you can also save the data in csv.
## Send Direct Message:
  1. send DM to any follower by getting id of that follower from all_followers.json
  2. save the follower details in send_dm.json as not to send auto dm again. 
