import requests, os, json, re

#Bearer Token
#何故かos.environにない
bearer_token = "AAAAAAAAAAAAAAAAAAAAAEqffgEAAAAAXIg2wGCJXs9Fbu5dOGxleSmzBWw%3D3o58JOtQN35aOIwhoAJJl7F3AJ9QLg90JWaG7nTkT35Yy2e74C"
#bearer_token = os.environ.get("BEARER_TOKEN")


def make_url():
    username = "usernames=username"
    #とりあえずフラグちゃんのuser_id使ってみた
    user_id = "1188782971932643328"
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
    pattern_url = "(https://t.co/[\w]*)"
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
            if check_url != "None":
                #つべの動画だったら埋め込み用の型式に整形する
                urls.append(re.sub(pattern_remove,pattern_replace,check_url.group()))
    return urls

def main():
    url = make_url()
    json_response = connect_to_endpoint(url)
    urls = get_url(json_response)
    print(urls)
    return urls


    
if __name__ == "__main__":
    main()