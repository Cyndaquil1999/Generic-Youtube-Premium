import requests, os, json, re, time

#Bearer Token
#何故かos.environにない
bearer_token = "AAAAAAAAAAAAAAAAAAAAAEqffgEAAAAA0tG4A4CYDOMO90xhKX62re4sDUg%3DM2ZEwCaf94QEtOUdG0DdLXrgySiPDvr8RRN1FxtOaHjN3CDDYC"
#bearer_token = os.environ.get("BEARER_TOKEN")
max_results = 10

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
        #flaskではinput使わないしtwitterAPI2のmainみたいにしてもいいかも...?
        username = input("TwitterのIDを入力してください: ")
        url = collect_userid.create_url(username)
        json_response = connect_to_endpoint(url)
        return json_response["data"][0]["id"]
        
def make_url(id):
    #userid = collect_userid
    #username = "usernames=<username>"
    #user_id = userid.main()
    #user_fields = "user_fields="
    #url = "https://api.twitter.com/2/users/by?{}".format(username)
    url = "https://api.twitter.com/2/users/{}/tweets?max_results={}".format(id, max_results)
    print(url)
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
    pattern_url = "(https://t.co/[\w]*)"
    #埋め込みするときにいらない部分を消す正規表現
    pattern_remove = "(watch\?v=)"
    #埋め込みするときにいらない部分をこれに置き換える
    pattern_replace = "embed/"
    #つべのurlだけをしょっぴく正規表現。後ろの方のはいらないのでカット
    pattern_youtube_url = "(https://www.youtube.com/watch\?v=[\w]*)"
    #つべのurlを入れるリスト
    urls = []
    tmp_list = []
    
    video_count = 0
    for i in a_dict["data"]:
        #print(i["text"])
        tmp_list += re.findall(pattern_url, str(i["text"]))
        #print("tweet_urls: {}".format(tweet_urls))
        
    #print(tmp_list)
    
    #短縮リンクを元に戻すためにgetをしている
    #ここがボトルネックなので、並列処理を行う
    #100件検索の参考値: 65sec(並列処理前)→5.44sec(並列処理実装後)
    
    with ThreadPoolExecutor(50) as exe:
        check_url = list(exe.map(requests.get, tmp_list))
        
    with ThreadPoolExecutor(50) as exe:
        check_url = list(exe.map(lambda x: x.url, check_url))
    
    #print(check_url)
    
    for j in range(len(check_url)):
        if video_count == 10:
            break
        #youtubeの動画リンクは実は長さ60固定で、頭から30文字見れば判定できてしまう
        if check_url[j][:30] == "https://www.youtube.com/watch?":
            #print(check_url[j], len(check_url[j]))
            video_count += 1
            urls.append(re.sub(pattern_remove, pattern_replace, check_url[j][:43]))
            
    return urls


def main():
    url = make_url()
    
    first_point = time.time()
    #print("開始〜API叩く前処理: {}".format(first_point - st))
    
    #type: dict
    json_response = connect_to_endpoint(url)
    
    second_point = time.time()
    #print("前処理〜API叩く: {}".format(second_point - first_point))
    
    urls = get_url(json_response)
    
    third_point = time.time()
    #print("動画取得: {:.2f}秒".format(third_point - second_point))
    
    #print("動画本数: {}本".format(len(urls)))
    return urls

def main(id):
    #uidは事前に求めるようにしたので、それを直接入れるように変えてみた
    url = make_url(id)
    json_response = connect_to_endpoint(url)
    tmp = json_response["data"]
    urls = get_url(json_response)
    return urls


    
if __name__ == "__main__":
    main()
