from newsfeat.lib.search_engine.searcher import Searcher
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    searcher = Searcher()
    search_data = {'query': request.args.get('query')}
    results = searcher.search(search_data)
    print(results)
    return results

if __name__ == "__main__":
    app.run()