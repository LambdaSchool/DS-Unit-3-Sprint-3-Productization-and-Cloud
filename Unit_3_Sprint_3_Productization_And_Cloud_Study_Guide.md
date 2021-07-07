This study guide should reinforce and provide practice for all of the concepts you have seen in the past week. There are a mix of written questions and coding exercises, both are equally important to prepare you for the sprint challenge as well as to be able to speak on these topics comfortably in interviews and on the job.

If you get stuck or are unsure of something remember the 20 minute rule. If that doesn't help, then research a solution with google and stackoverflow. Only once you have exausted these methods should you turn to your Team Lead - they won't be there on your SC or during an interview. That being said, don't hesitate to ask for help if you truly are stuck.

Have fun studying!

# Questions of Understanding
1. Define the following and give an example of an appropriate task for each:
 - Front-end:
 - Back-end:
 - Database:
2. What is a decorator?
3. What is a route?
4. Why do we want to separate our code into separate files when writing an application? Why not just one big file?
5. What is an API? Give an example of an API that is not Twitter's.
6. What does it mean to pickle a model? Why might this be useful?

# Basics of Flask

## Coding
Write a Flask application that displays "Hello World!" to the local host (usually `127.0.0.1:5000` or `localhost:5000`)

## Questions of Understanding
1. Flask is described as a "microframework" for developing web applications. What is a "microframework"?
2. What is another web development framework in Python?
3. In this line of code: `APP = Flask(__name__)` What does `__name__` do?
4. What line of your code tells when and where "Hello World!" should be displayed?
5. What do we need to type into the terminal to run our flask application?

# API's

## Coding
API's are a common part of programming, whether setting up your own or using someone else's. Today we will be looking at the API for the board gaming hobby site BoardGameGeek (BGG). The API instructions can be found [here](https://boardgamegeek.com/wiki/page/BGG_XML_API&redirectedfrom=XML_API#). There are many wrappers online for the BGG API that you may use but the sample code below will use `requests` and the web scraping library `BeautifulSoup`.

```python
import requests
import bs4

game_id = 13
url = 'https://www.boardgamegeek.com/xmlapi/boardgame/' + str(game_id)
result = requests.get(url)
soup = bs4.BeautifulSoup(result.text, features='lxml')
print(soup.find('name').text)
```

The code above uses the API to search for a game by its ID number (more than 16,000 entries on BGG). Once the API returns the results, BeautifulSoup is used to parse the XML and make it easily searchable.

Explore the BGG API and see if you are able to find the following information about a game:
- Name
- Max and Min Players
- Play Time
- Game Description
- Some of the game mechanics

# Flask and Databases

## Code
Write a Flask web application using `SQLAlchemy` with the following:
- A home route that displays at least one entry from a database of stored BGG game information
- A dynamic route `/add/<game_id>` that adds game information into your database based on the ID in the route.
- A route that resets the database
- The database should have the following following columns as a minimum: id (integer), name (string), and max_players (integer)

## Questions of Understanding
1. What line of code establishes what database should be used for your application?
2. How do we define our table, what columns are going to be in it, and what those column datatypes are?
3. How do we make a query to our database?

# HTML Templates

## Code
Create a small HTML template to display all the games in your database. Update your home route to use this template.

## Questions of Understanding
1. What is an HTML template?
2. What module do we need to import from `flask` to use our HTML template?

# Heroku

## Code
It is not necessary, but you can try putting your app on Heroku

## Questions of Understanding
1. What is a platform-as-a-service?
2. Why do we need to use a service like Heroku? Why not just host the application on our local machine?
