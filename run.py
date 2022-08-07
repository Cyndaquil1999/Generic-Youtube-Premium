from flask import Flask, render_template, request
import twitterAPI2, download, twitterAPI
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')
 
@app.route('/getid',methods=["GET"])
def getid():
    userid = twitterAPI2.main(request.args.get("id"))
    return render_template('test.html',id=userid,flag=twitterAPI.main(userid["data"][0]["id"]))

@app.route('/download_movie',methods=["GET"])
def download_movie():
    download.main(request.args.get("url"))
    return "終わったよ"

if __name__ == '__main__':
    app.run()
