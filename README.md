# Welcome to Newsfeat

A demo of this project is available at: http://cs410.fpinvidio.com

A video presentation explaining the basics for this project is available at: http://cs410.fpinvidio.com 

### What's all the fuss about?

People dedicated to content generation rely on relevant news for building their compositions.
Current search engines depend strictly on the user's query and don't take into account other variables such as user interests.
A massive amount of news are created every day making it impossible for a human to process that much information in an adequate time.

That's where Newsfeat comes in, a feature based News Recommendation Engine. Newsfeat suggests relevant news based on your specific interests or a set of important features at a specific time. And for each recommended news presented it extracts phrases that answer the most important questions that describe the article’s event. **Who, What, When, Where, Why and How?**

### For who?

Writers, content-generators or people looking to read relevant articles and extract the most significant information in a timely fashion will benefit from it. Available tools that solve some of these problems in an independent way have been around for several years. But the way Newsfeat aims to combine them in order to reduce searching and processing time is definitely innovative.

### How did you manage to build this?

#### Project structure

* htdocs
  * directory container for the Newsfeat Flask webapp.
* news-please
  * contains the news crawler config and initial extracted data
* db
  * contains an mongo export required for running the project
* scripts
  * additional scripts for processing

#### The dataset

It's starts by retrieving the news articles. News crawler [news-please](https://github.com/fhamborg/news-please) was used for extracting articles from The New York Times web.
About 10K were successfully extracted as json files in a specific directory structure. For that reason some pre-processing was needed before running the indexing.
A script that searched through the directories, found the files, parsed the extracted news json and generated txts with the article text as a line was implemented.
The script called [news-processor](https://github.com/fpinvidio/newsfeat/blob/master/scripts/news-processor.py) user for this operation is available in the scripts folder.
About a 5% of the articles were a default maintenance message from NY Times, those were excluded from the dataset.  
Additionally, the extracted json information was stored in a MongoDB database for simplifying information querying.

#### Search engine feature

News data was correctly indexed and Okapi BM25 is being used for the search engine feature.
Initially metapy was used in the project for searching, due to encountered errors which difficulted the realization of the project it was changed for [Whoosh](https://whoosh.readthedocs.io/en/latest/), a fast search engine library for python and continuing using Okapi BM25 as algorithm for ranking.
Indexing of the dataset is required prior for searching. For that, the [indexer.py](https://github.com/fpinvidio/newsfeat/blob/master/htdocs/newsfeat/indexer.py) has the Indexer class with an index method.
```python
class Indexer:
    def __init__(self, root, idx_path):
        """
        Defines the corpus folder name and the to be generated index path.
        """
        self.root = root
        self.idx_path = idx_path

    def index(self):

        """
        Defines a schema for processing the file.
        """
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), \
                        content=TEXT, textdata=TEXT(stored=True))
        if not os.path.exists(self.idx_path):
            os.mkdir(self.idx_path)

        # Creating a index writer to add document as per schema
        ix = create_in(self.idx_path, schema)
        writer = ix.writer()

        filepaths = [os.path.join(self.root, i) for i in os.listdir(self.root)]
        for path in filepaths:
            with codecs.open(path, "r", "utf-8") as f:
                content = f.read()
                writer.add_document(title=unicode(path.split("/")[1]), path=unicode(path.split("/")[0]), \
                                    content=content, textdata=content)
        writer.commit()
        return "true"
```

The script [searcher.py](https://github.com/fpinvidio/newsfeat/blob/master/htdocs/newsfeat/searcher.py) contains the class Searcher. It recieves an index path for initialization and contains a search method that returns a json with the result. 

```python
class Searcher:
    """
    Wraps the Whoosh search engine and its rankers.
    """
    def __init__(self, idx_path):
        """
        Load the inverted index based on the provided index_path.
        """
        self.ix = open_dir(idx_path)

    def search(self, search_term):
        topN = 10
        client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
        db = client.newsfeat
        news = db.news
        response = {'query': search_term, 'results': []}
        start = time.time()
        with self.ix.searcher(weighting=scoring.Frequency) as searcher:
            query = QueryParser("content", self.ix.schema).parse(search_term)
            results = searcher.search(query, limit=topN)
            count = len(results) if len(results) < topN else topN
            for i in range(count):
                result = news.find({'file_path': results[i]['title']})
                for doc in result:
                    response['results'].append(doc)
        response['elapsed_time'] = time.time() - start
        return json.dumps(response,default=json_util.default)
```

#### Recommender engine feature

For the article recommendation [LightFM](http://lyst.github.io/lightfm/docs/index.html) library was used. LightFM is a Python implementation of a number of popular recommendation algorithms for both implicit and explicit feedback.
Collaborative filtering including WARP ranking losses is used for recommending articles.
For simplicity of the project only five users are available on the system, for supporting more a refactor would be required.
Like and dislike buttons are available for every news, so that users may input the feedback. 

[recommender.py](https://github.com/fpinvidio/newsfeat/blob/master/htdocs/newsfeat/recommender.py) contains a Recommender class with a recommend method that returns relevant articles for a specific user with some prior training. 

```python
class Recommender:
    """
    Trains the data.
    """
    def __init__(self):
        client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
        #client = MongoClient()
        db = client.newsfeat
        news = db.news
        # news.update_many({}, {"$set" : {"user_likes": [0, 0, 0, 0, 0]}})
        train = list(news.find({}, {'user_likes': 1, '_id': 0}))

        def extract_likes(col):
            return col['user_likes']

        def extract_ids(col):
            return col['_id']

        train = map(extract_likes, train)
        train = map(list, zip(*train))
        train = coo_matrix(train)
        model = LightFM(loss='warp')
        model.fit(train, epochs=20)

        items = list(news.find({}, {'_id': 1}))
        items = np.array(map(extract_ids, items))
        self.model = model
        self.items = items
        self.train = train

    def recommend(self, user_ids):
        client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
        db = client.newsfeat
        news = db.news
        # number of users and news in training data
        n_users, n_items = self.train.shape
        # generate recommendations for each user we input
        response = {'results': []}
        for user_id in user_ids:
            # news our model predicts they will like
            scores = self.model.predict(user_id, np.arange(n_items))
            # rank them in order of most liked to least
            top_items = list(self.items[np.argsort(-scores)])
            top_items = top_items[:10]
            top_news = list(news.find({'_id': {'$in': list(top_items)}}))
            response['results'] = top_news
        return json.dumps(response, default=json_util.default)
```

#### Who, What, Where, When, Why and How?

[Giveme5W1H](https://github.com/fhamborg/Giveme5W1H) was integrated in the project for extracting answers to a news article most relevant questions. Articles were preprocessed offline and answers were saved along the collection in the MongoDB database. Due to the processing time for the answer extraction for each article, about 4200 articles were preproccessed.

#### Web interface

Django was the first choice for web framework at the beginning, but due to incompatibilities with the metapy library it was changed for Flask.
Flask is a very simple microframework for Python. Within the [\_\_init__.py](https://github.com/fpinvidio/newsfeat/blob/master/htdocs/newsfeat/__init__.py) are all the routes available for the web application.
[Bootstrap](https://getbootstrap.com/), an open source toolkit, was used for building the webapp. jQuery was also used for executing the ajax GET and POST requests.

Within the templates dir you'll find the index.html which contains the [index.html](https://github.com/fpinvidio/newsfeat/blob/master/htdocs/newsfeat/templates/index.html) used in the webapp.
The following shows the available API methods for the flask application: 
```python
"""
    Index route for rendering the index.html template
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
    Route used for searching. Receives a query param and returns a json with all the results.
"""
@app.route('/search')
def search():
    searcher = Searcher("/var/www/cs410.fpinvidio.com/htdocs/newsfeat/htdocs/newsfeat/idx")
    #searcher = Searcher("idx")
    return searcher.search(request.args.get('query'))

"""
    Route used for recommending. Receives a user_id param for specifying the user and returns a json with all the results.
"""
@app.route('/recommend')
def recommend():
    recommender = Recommender()
    user_id = int(request.args.get('user_id'))-1
    return recommender.recommend([user_id])

"""
    POST Route used for liking an article. An id param is used for specifying
    the article and a user_id param is for identifying the user.
"""
@app.route('/news/<string:id>/like', methods=['POST'])
def like_news(id):
    client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
    #client = MongoClient()
    db = client.newsfeat
    news = db.news
    article = news.find_one({'_id': ObjectId(id)})
    if article is not None:
        user_likes = article['user_likes']
        user_id = int(request.form.get('user_id')) - 1
        user_likes[user_id] = 1
        news.update({'_id': ObjectId(id)}, {"$set": {"user_likes": user_likes}})
        return "{success: true}"
    return "{success: false}"

"""
    POST Route used for disliking an article. An id param is used for specifying
    the article and a user_id param is for identifying the user.
"""
@app.route('/news/<string:id>/dislike', methods=['POST'])
def dislike_news(id):
    client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
    #client = MongoClient()
    db = client.newsfeat
    news = db.news
    article = news.find_one({'_id': ObjectId(id)})
    if article is not None:
        user_likes = article['user_likes']
        user_id = int(request.form.get('user_id')) - 1
        user_likes[user_id] = -1
        news.update({'_id': ObjectId(id)}, {"$set": {"user_likes": user_likes}})
        return "{success: true}"
    return "{success: false}"

"""
    Additional route used for indexing the dataset.
"""
@app.route('/search_index')
def search_index():
    indexer = Indexer("data", "/var/www/cs410.fpinvidio.com/htdocs/newsfeat/htdocs/newsfeat/idx")
    #indexer = Indexer("data", "idx")
    return indexer.index()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
```

#### Web server

The demo is deployed on an Amazon EC2 instance with ubuntu. Apache is beign used as web server along the wsig module.

### How can I get this up and running?

#### Prerequisites

MongoDB and Python 2.7 are requirements for this project. Please refer to their corresponding documentations for getting them up and running.

#### Dependencies

This project has a dependency on the following libraries:

* Numpy
* Scipy
* Whoosh
* LightFM
* news-please
* Giveme5W1H
* Pymongo
* Flask
* Json

You can use the requirements.txt located within the htdocs folder for an automated dependecy installation using the following: 
```
pip install -r requirements.txt
```
Currently this file has a specific dependancy(PyObjc) for OSX due to the LightFM library, therefore installing this library in other systems will produce an error. For that reason it is recommended to install separately.

Or by running the following:

```
pip install numpy scipy pymongo flask whoosh lightfm
``` 

#### Importing the database

```
mongoimport --db newsfeat --collection news --file newsfeat.news.json
```

#### Running the server

```
cd htdocs/newsfeat/
python __init__.py
``` 

The server will start running at the following URL: [http://0.0.0.0:5000/](http://0.0.0.0:5000/)


### Can we get in touch?

Sure, send me an email at [fp6@illinois.edu](mailto:fp6@illinois.edu) and i'll try to get back to you as soon as I can.

# Have fun!