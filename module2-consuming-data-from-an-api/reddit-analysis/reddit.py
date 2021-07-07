import os
import requests
import requests.auth
from dotenv import load_dotenv

load_dotenv()

user_agent = "LambdaAnalysisClient/0.1 by " + os.getenv("REDDIT_USERNAME")

def get_auth_info():
    client_auth = requests.auth.HTTPBasicAuth(os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_CLIENT_SECRET"))
    post_data = {"grant_type": "password", "username": os.getenv("REDDIT_USERNAME"), "password": os.getenv("REDDIT_PASSWORD")}
    headers = {"User-Agent": user_agent}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    print(response.json())
    return response.json()

def make_request(auth_info):
    headers = {"Authorization": f"bearer {auth_info['access_token']}", "User-Agent": user_agent}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    return response.json()

print(make_request(get_auth_info()))