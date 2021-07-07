# Consuming Data from an API

A data-backed application is only as good as the data it has - and a great way
to get a lot of data is through an API. The idea of an API is actually very
general, but in the modern day usually refers to "asking some other service to
give you (some of) their data." A lot of apps are built this way, especially
when starting out, but there are some steps and hoops to get it working.

## Learning Objectives

- Connect to the Twitter API and query for tweets by various parameters
- Implement a SpaCy NLP model to create embeddings from our tweet text.

## Before Lecture

Sign up for [Twitter Developer
access](https://developer.twitter.com/en/apply-for-access) - this requires
answering various questions about what you will use the API for. Answer
honestly, mentioning that you are a student and will be developing an
application that analyzes the textual content of Tweets for comparing different
Twitter users. Also check out [Tweepy](https://tweepy.readthedocs.io/), a Python
package that facilitates accessing the Twitter API.

Explore the [SpaCy](https://spacy.io/usage/spacy-101). This service will 
let you use the [word2vect](https://en.wikipedia.org/wiki/Word2vec) to fit
predictive models such as regression to numerical data. This allows us to work
with things data scientist like most - digits - opposed to unstructured words.
These numbers are referred to as "embeddings" - the numbers representing the words 
or phrases from the vocabulary.

## Live Lecture Task

We'll get set up to access the Twitter API and add the SpaCy model to our Flask
application, using environment variables (facilitated with
[python-dotenv](https://github.com/theskumar/python-dotenv)) to ensure we
don't check any secrets into git.

## Assignment

Reproduce the steps from lecture (ensure you can access both the Twitter API 
and SpacCy package & model via Python), then:

- Write methods to pull actual Users and Tweets and replace your invented data
  with actual Twitter data
- Add an `embedding` (the representative numbers) field to your `Tweet` model, and functions to populate it
  with embeddings returned from the implemented SpaCy model.
  

## Resources and Stretch Goals

- Add a `/user/<name>` route and template that pulls and displays user Tweets
- [Flask routing](http://flask.pocoo.org/docs/1.0/quickstart/#routing) is simple
  but powerful - take advantage of it!
- [https://www.getpostman.com/](Postman) is an app to let you test both your
  routes and a REST API
- Go deeper with the Twitter API - use paging (offset by oldest fetched Tweet
  ID) to pull older Tweets, so you can build a larger set of embedding data for
  a given user
- [twitter-scraper](https://github.com/kennethreitz/twitter-scraper) is another
  approach to getting data from Twitter - no auth required (but Twitter may
  choose to try to break it)
- Make the home page a bit more useful - links to pulled users, descriptive
  text, etc.
- Make your app look nicer - the earlier mentioned [Picnic
  CSS](https://picnicss.com) is an easy way, and
  [Bootstrap](https://getbootstrap.com) is very widely used
- You may notice that pulling lots of Tweets and getting lots of embeddings
  takes a long time (and may even be rate limited) - organize your code in
  functions so these tasks can be performed "offline" (without loading the full
  Flask application)
- Try using some of the other information form the Twitter API and maybe figure out
  what information from the API might be fun to play with and store in our database.
  
  
## Twitter Developer Account Alternative
If you are having trouble getting access to a Twitter developer account check out [this API](https://lambda-ds-twit-assist.herokuapp.com/) that
will allow you to make HTTP GET request to a third party API to get back information about a specific user. 

All you need to do is utilize the `requests` library and make a get request to the following url and specifiy the user within the endpoint.
```python
https://lambda-ds-twit-assist.herokuapp.com/user/<twitter_handle>
```
Then you need to populate the values and ids into the database with SQLAlchemy. An example of a request may look like the following:
```python
import ast # for unpacking the literal string object 
import requests

status = requests.get("https://lambda-ds-twit-assist.herokuapp.com/user/elonmusk")
elon = ast.literal_eval(status.text)
```
