from flask import Flask, render_template 
import twitterAPI
app = Flask(__name__)
 
@app.route('/')
def hello():
    return render_template('index.html',flag = twitterAPI.main())
 
@app.route('/channel')
def flagchan():
    return twitterAPI.main()

if __name__ == '__main__':
    app.run()