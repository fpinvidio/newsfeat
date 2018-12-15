from searcher import Searcher
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    search_data = 'London'#request.args.get('query')}
    execfile('search-processor.py')
    return "Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
