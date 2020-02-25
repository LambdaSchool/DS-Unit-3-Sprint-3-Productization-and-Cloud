###Module 1 Assignment
I was able, with a little trial and error, 
to get all the required packages installed and running, as well as
get my app to run properly. I was pleased that I was able to get 
my app to route to new HTML files I created instead of just outputting
the success and error messages. 

I'm having trouble inserting new tweets into my database mostly because
I'm not sure how to connect the form with the user names to a new 
form for making tweets so that only established users can tweet,
 and then insert that while refering the user_id
from the user table. But I can do it manually through TablePlus. 

Working simultaneously with Python scripts and HTML files is different
than what I'm used to. If I have script and it outputs something
unexpected, I can generally find that piece of code fairly quickly
just by scanning for keywords. But in this case, the text of one page 
is determined by a combination of the Python script and the HTML file
so it's harder to figure out where something unexpected is coming from. 

###Module 2 Assignment
I'm enjoying the Basilica package. I worked it into another side project
that I am working on (a Kaggle competition about analyzing tweets 
about disasters). 

I was able to work out the syntax for the Tweep library but I'm having more
trouble with SQLAlchemy. I think I can get it, though, it's just a matter of
taking more time to read the documentation. My goal is to get the web app to
dynamically update the tweets table with the most recent tweet from a user when
they are added to the database.

###Module 3 and 4
I was able to get my Flask app written and deployed to Heroku. Right now, I can use it
to add users to a database, see their recent tweets, and determine which of those
recent tweets has had the most interaction. 

I'm trying to build a model to predict how many interactions a new tweet will
have, based on the behavior of a user's followers in the past. I'm running into 
issues formatting the data so it fits into the model. I'll keep working on that
leading into the weekend. 