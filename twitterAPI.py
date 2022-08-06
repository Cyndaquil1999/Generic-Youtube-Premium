import requests, os, json, re

#Bearer Token
#何故かos.environにない
bearer_token = "AAAAAAAAAAAAAAAAAAAAAEqffgEAAAAA0tG4A4CYDOMO90xhKX62re4sDUg%3DM2ZEwCaf94QEtOUdG0DdLXrgySiPDvr8RRN1FxtOaHjN3CDDYC"
#bearer_token = os.environ.get("BEARER_TOKEN")
max_results = 30

class collect_userid:
    def create_url(user):
        usernames = f"usernames={user}"
        url = f"https://api.twitter.com/2/users/by?{usernames}"
        return url


    def bearer_oauth(r):
        r.headers["Authorization"] = f"bearer {bearer_token}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r


    def connect_to_endpoint(url):
        response = requests.request("GET", url, auth=bearer_oauth,)
        #print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
    def main():
        username = input("TwitterのIDを入力してください: ")
        url = collect_userid.create_url(username )
        json_response = connect_to_endpoint(url)
        return json_response["data"][0]["id"]
        
def make_url():
    userid = collect_userid
    username = "usernames=<username>"
    user_id = userid.main()
    #user_fields = "user_fields="
    #url = "https://api.twitter.com/2/users/by?{}".format(username)
    url = "https://api.twitter.com/2/users/{}/tweets?max_results={}".format(user_id, max_results)
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

"""
ツイート内の短縮urlを全て調べ上げ、そこからさらにつべのurlだけを抽出して返す関数
a_dict:取得したツイートが入った辞書
urls:つべのurlを入れたリスト
"""
def get_url(a_dict):
    #全ての短縮urlをしょっぴく正規表現
    pattern_url = "(https://t.co/[\w\-]*)"
    #埋め込みするときにいらない部分を消す正規表現
    pattern_remove = "(watch\?v=)"
    #埋め込みするときにいらない部分をこれに置き換える
    pattern_replace = "embed/"
    #つべのurlだけをしょっぴく正規表現。後ろの方のはいらないのでカット
    pattern_youtube_url = "(https://www.youtube.com/watch\?v=[\w]*)"
    #つべのurlを入れるリスト
    urls = []
    for i in a_dict["data"]:
        #print(i["text"])
        tweet_urls = re.findall(pattern_url, str(i["text"]))
        #最後のurlは取得したツイートのurl。絶対使わないのでそれ以外をurlsにぶち込む
        for j in range(len(tweet_urls) - 1):
            check_url = re.search(pattern_youtube_url,requests.get(tweet_urls[j]).url)
            #print(check_url)
            if str(check_url) != "None":
                #つべの動画だったら埋め込み用の型式に整形する
                urls.append(re.sub(pattern_remove,pattern_replace,str(check_url.group())))
    return urls

def main():
    url = make_url()
    json_response = connect_to_endpoint(url)
    tmp = json_response["data"]
    for i in range(len(tmp)):
        print(tmp[i]["text"]+"\n")
    urls = get_url(json_response)
    print(urls)
    return urls


    
if __name__ == "__main__":
    main()