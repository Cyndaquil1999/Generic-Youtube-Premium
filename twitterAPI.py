import requests, os, json

#Bearer Token
#何故かos.environにない
bearer_token = "<BEARER_TOKEN>"
#bearer_token = os.environ.get("BEARER_TOKEN")


def make_url():
    username = "usernames=<username>"
    user_id = "<user_id>"
    #user_fields = "user_fields="
    #url = "https://api.twitter.com/2/users/by?{}".format(username)
    url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
    return url

    

def bearer_oauth(r):
    r.headers["Authorization"] = f"bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    return response.json()


def main():
    url = make_url()
    
    #type: dict
    json_response = connect_to_endpoint(url)

    #type: list
    tmp = json_response["data"]
    
    for i in range(len(tmp)):
        print(tmp[i]["text"]+"\n")
    
    
    #type: str
    #json_response = json.dumps(json_response, indent=4, sort_keys=True)
    
if __name__ == "__main__":
    main()