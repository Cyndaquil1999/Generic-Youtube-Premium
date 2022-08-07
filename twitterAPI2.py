import requests, json
from twitterAPI import collect_userid

#別ファイルってこういうこと...?
def main(id):
    #username = input("TwitterのIDを入力してください: ")
    url = collect_userid.create_url(id)
    json_response = collect_userid.connect_to_endpoint(url)
    return json_response
    
if __name__ == "__main__":
    main(id)
