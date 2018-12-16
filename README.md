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

#### The dataset

It's starts by retrieving the news articles. News crawler [news-please](https://github.com/fhamborg/news-please) was used for extracting articles from The New York Times web.
About 10K were successfully extracted as json files in a specific directory structure. For that reason some pre-processing was needed before running the indexing.
A script that searched through the directories, found the files, parsed the extracted news json and generated txts with the article text as a line was implemented.
The script called [news-processor](https://github.com/fpinvidio/newsfeat/blob/master/scripts/news-processor.py) user for this operation is available in the scripts folder.
Additionally, the extracted json information was stored in a MongoDB database for simplifying information querying.

#### Search engine feature

News data was correctly indexed and Okapi BM25 is being used for the search engine feature.
Initially metapy was used in the project for searching, due to encountered errors which difficulted the realization of the project it was changed for [Whoosh](https://whoosh.readthedocs.io/en/latest/), a fast search engine library for python and continuing using Okapi BM25 as algorithm for ranking.

#### Recommender engine feature

For the article recommendation [LightFM](http://lyst.github.io/lightfm/docs/index.html) library was used. LightFM is a Python implementation of a number of popular recommendation algorithms for both implicit and explicit feedback.

#### Who, What, Where, When, Why and How?

[Giveme5W1H](https://github.com/fhamborg/Giveme5W1H) was integrated in the project for extracting answers to a news article most relevant questions. Articles were preprocessed offline and answers were saved along the collection in the MongoDB database. Due to the processing time for the answer extraction for each article, about 4200 articles were preproccessed.

#### Web interface

Django was the first choice for web framework at the beginning, but due to incompatibilities with the metapy library it was changed for Flask.
Flask is a very simple microframework for Python. Within the [\_\_init__.py](https://github.com/fpinvidio/newsfeat/blob/master/htdocs/newsfeat/__init__.py) are all the routes available for the web application.
[Bootstrap](https://getbootstrap.com/), an open source toolkit, was used for building the webapp.

#### Web server

The demo is deployed on an Amazon EC2 instance with ubuntu. Apache is beign used as web server along the wsig module.

### How can I get this up and running?

#### Prerequisites

MongoDB and Python 2.7 are requirements for this project. Please refer to their corresponding documentations for getting them up and running.

#### Dependacies

pip install -r requirements.txt

#### Running the server

### Can we get in touch?

Sure, send me an email at [fp6@illinois.edu](mailto:fp6@illinois.edu) and i'll try to get back to you as soon as I can.

# Thanks